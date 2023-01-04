# SPDX-License-Identifier: MIT

import typing as t

from typing_extensions import Self

__all__ = ("classproperty",)

T = t.TypeVar("T")


class classproperty(t.Generic[T]):
    def __init__(self, fget: t.Callable[[t.Any], T], /) -> None:
        self.fget: "classmethod[T]"
        self.getter(fget)

    def getter(self, fget: t.Callable[[t.Any], T], /) -> Self:
        if not isinstance(fget, classmethod):
            raise ValueError(f"Callable {fget.__name__} is not a classmethod!")

        self.fget = fget
        return self

    def __get__(self, obj: t.Optional[t.Any], type: t.Optional[type]) -> T:
        return self.fget.__func__(type)
