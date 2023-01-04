# SPDX-License-Identifier: MIT

from __future__ import annotations

import asyncio
import inspect
import logging
import sys
import traceback
import typing as t
from collections import defaultdict
from importlib import reload

import attr
from typing_extensions import Self, TypeGuard

from .event import Event, EventT, ExceptionEvent
from .json import JSONObject

if t.TYPE_CHECKING:
    from ..gateway import GatewayClient

if sys.version_info >= (3, 10):
    from types import UnionType

    _union_types = {t.Union, UnionType}
else:
    _union_types = {t.Union}

_log = logging.getLogger(__name__)

__all__ = (
    "Consumer",
    "consumer_for",
    "Dispatcher",
)

T = t.TypeVar("T")
DispatcherT = t.TypeVar("DispatcherT", bound="Dispatcher")
ListenerCallbackT = t.TypeVar("ListenerCallbackT", bound="ListenerCallback[Event]")
Coro = t.Coroutine[T, t.Any, t.Any]

ListenerCallback = t.Callable[[EventT], Coro[None]]
ConsumerCallback = t.Callable[[DispatcherT, "GatewayClient", JSONObject], Coro[None]]


# ported from discatpy
def _get_globals(x: object) -> dict[str, t.Any]:
    module = inspect.getmodule(x)

    if module:
        try:
            t.TYPE_CHECKING = True
            reload(module)
        except ModuleNotFoundError:
            # incomplete __main__ module
            # this does mean that anything defined in TYPE_CHECKING will not be extracted
            # TODO: find an alternative solution for __main__ module that extracts items from TYPE_CHECKING statements
            pass
        finally:
            t.TYPE_CHECKING = False

    return module.__dict__


@attr.define
class Consumer(t.Generic[DispatcherT]):
    """Represents a dispatcher consumer. A consumer consumes a raw event and performs actions based on the raw event."""

    callback: ConsumerCallback[DispatcherT]
    events: tuple[type[Event], ...]


def consumer_for(
    *event_types: type[Event],
) -> t.Callable[[ConsumerCallback[DispatcherT]], Consumer[DispatcherT]]:
    event_types = tuple({event for event_type in event_types for event in event_type.dispatches})

    def wrapper(func: ConsumerCallback[DispatcherT]) -> Consumer[DispatcherT]:
        return Consumer(func, event_types)

    return wrapper


def _is_exception_event(e: EventT) -> TypeGuard[ExceptionEvent[EventT]]:
    return isinstance(e, ExceptionEvent)


class Dispatcher:
    """A class that helps manage events."""

    __slots__ = ("_listeners", "_consumers")

    def __init__(self) -> None:
        self._listeners: defaultdict[type[Event], list[ListenerCallback[Event]]] = defaultdict(
            lambda: []
        )
        self._consumers: dict[str, Consumer[Self]] = {}

        for name, value in inspect.getmembers(self):
            if not isinstance(value, Consumer):
                continue

            self._consumers[name.lower()] = value

    async def _run_listener(self, event: EventT, listener: ListenerCallback[EventT]) -> None:
        try:
            await listener(event)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            if _is_exception_event(event):
                _log.error(
                    "There was an error while running the listener callback (%s%s) under exception event %s.%s: %s",
                    listener.__name__,
                    inspect.signature(listener),
                    type(event).__module__,
                    type(event).__qualname__,
                    traceback.format_exception(type(e), e, e.__traceback__),
                )
            else:
                exec_event = ExceptionEvent(
                    exception=e, failed_event=event, failed_listener=listener
                )

                _log.info(
                    "An exception occured while handling %s.%s.",
                    type(event).__module__,
                    type(event).__qualname__,
                )
                await self.dispatch(exec_event)

    async def _handle_consumer(
        self, consumer: ConsumerCallback[Self], gateway: GatewayClient, payload: JSONObject
    ):
        try:
            await consumer(self, gateway, payload)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            asyncio.get_running_loop().call_exception_handler(
                {
                    "message": "An exception occured while consuming a raw event.",
                    "exception": e,
                    "task": asyncio.current_task(),
                }
            )

    def subscribe(self, event: type[EventT], func: ListenerCallback[EventT]) -> None:
        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f"listener callback {func.__name__!r} has to be a coroutine function!")

        _log.debug(
            "Subscribing listener callback (%s%s) to event %s.%s",
            func.__name__,
            inspect.signature(func),
            event.__module__,
            event.__qualname__,
        )
        self._listeners[event].append(func)  # pyright: ignore

    def unsubscribe(self, event: type[EventT], func: ListenerCallback[EventT]) -> None:
        listeners = self._listeners.get(event)
        if not listeners:
            return

        _log.debug(
            "Unsubscribing listener callback (%s%s) from event %s.%s",
            func.__name__,
            inspect.signature(func),
            event.__module__,
            event.__qualname__,
        )
        listeners.remove(func)  # pyright: ignore

        if not listeners:
            del self._listeners[event]

    @t.overload
    def listen_to(
        self, func: ListenerCallback[EventT], *, events: None = ...
    ) -> ListenerCallback[EventT]:
        pass

    @t.overload
    def listen_to(
        self, func: ListenerCallback[EventT], *, events: list[type[EventT]]
    ) -> t.NoReturn:
        pass

    @t.overload
    def listen_to(
        self, func: None = ..., *, events: list[type[EventT]]
    ) -> t.Callable[[ListenerCallback[EventT]], ListenerCallback[EventT]]:
        pass

    @t.overload
    def listen_to(
        self, func: None = ..., *, events: None = ...
    ) -> t.Callable[[ListenerCallback[EventT]], ListenerCallback[EventT]]:
        pass

    def listen_to(
        self,
        func: t.Optional[ListenerCallback[EventT]] = None,
        *,
        events: t.Optional[list[type[EventT]]] = None,
    ) -> t.Union[
        t.Callable[[ListenerCallback[EventT]], ListenerCallback[EventT]],
        ListenerCallback[EventT],
        t.NoReturn,
    ]:
        if func and events is not None:
            raise ValueError(f"func and events parameters cannot both be set!")

        def wrapper(func: ListenerCallback[EventT]) -> ListenerCallback[EventT]:
            func_sig = inspect.signature(func)
            event_arg = next(iter(func_sig.parameters.values()))
            event_arg_anno = event_arg.annotation

            resolved_events: set[type[Event]]
            if event_arg_anno is inspect.Parameter.empty:
                if events:
                    resolved_events = set(events)
                else:
                    raise TypeError(
                        "No event type was provided! Please provide it as an argument or a type hint."
                    )
            else:
                if isinstance(event_arg_anno, str):
                    event_arg_anno = eval(event_arg_anno, _get_globals(func))

                def event_check(arg: t.Any) -> None:
                    if not isinstance(arg, type) and not issubclass(arg, Event):
                        raise TypeError(f"Expected an event, got {arg!r}.")

                if t.get_origin(event_arg_anno) in _union_types:
                    union_args = t.get_args(event_arg_anno)

                    for arg in union_args:
                        event_check(arg)

                    resolved_events = t.cast(set[type[Event]], set(union_args))
                else:
                    event_check(event_arg_anno)
                    resolved_events = {t.cast(type[Event], event_arg_anno)}

            for event in resolved_events:
                self.subscribe(event, func)  # pyright: ignore

            return func

        if func:
            return wrapper(func)
        return wrapper

    def dispatch(self, event: Event) -> asyncio.Future[t.Any]:
        _log.debug(
            "Dispatching event %s.%s (which dispatches event(s) %r).",
            type(event).__module__,
            type(event).__qualname__,
            [f"{e.__module__}.{e.__qualname__}" for e in event.dispatches],
        )
        dispatched: t.List[Coro[None]] = []

        for event_type in event.dispatches:
            for listener in self._listeners.get(event_type, []):
                dispatched.append(self._run_listener(event, listener))

        def _completed_future() -> asyncio.Future[None]:
            future = asyncio.get_running_loop().create_future()
            future.set_result(None)
            return future

        return asyncio.gather(*dispatched) if dispatched else _completed_future()

    def consume(self, event: str, gateway: GatewayClient, payload: JSONObject):
        consumer = self._consumers.get(event)

        if not consumer:
            _log.info("Consumer %s does not exist. Skipping consumption.", event)
            return

        _log.debug("Consuming raw event %s.", event)
        asyncio.create_task(
            self._handle_consumer(consumer.callback, gateway, payload),
            name=f"DisCatCore Consumer {event}",
        )
