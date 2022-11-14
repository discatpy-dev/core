# SPDX-License-Identifier: MIT

import typing as t

from discatcore.types import Unset, UnsetOr, _UnsetEnum  # pyright: ignore[reportPrivateUsage]


def test_unset():
    assert bool(Unset) == False
    assert repr(Unset) == "Unset"
    assert str(Unset) == "Unset"


def test_unsetor():
    assert UnsetOr[int] == t.Union[int, _UnsetEnum]
