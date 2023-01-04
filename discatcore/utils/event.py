# SPDX-License-Identifier: MIT

from __future__ import annotations

import typing as t

import attr

from .functools import classproperty

if t.TYPE_CHECKING:
    from .dispatcher import ListenerCallback

__all__ = ("Event", "ExceptionEvent")

EventT = t.TypeVar("EventT", bound="Event")


class Event:
    """Represents a dispatcher event. An event class contains information about an event for use in listeners."""

    __slots__ = ()

    __dispatches: tuple[type[Event], ...]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        cls.__dispatches = tuple(base for base in cls.__mro__ if issubclass(base, Event))

    @classproperty
    @classmethod
    def dispatches(cls):
        return cls.__dispatches


@attr.define(kw_only=True)
class ExceptionEvent(Event, t.Generic[EventT]):
    """An event that is dispatched whenever a dispatched event raises an exception."""

    exception: BaseException
    failed_event: EventT
    failed_listener: ListenerCallback[EventT]
