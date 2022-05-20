from __future__ import annotations

from typing import Any, Type, TypeVar

T = TypeVar('T')
T_OUT = TypeVar('T_OUT')


def type_filter(value: Any, t: Type[T_OUT], allow_None=True) -> T_OUT:
    if value is None and allow_None:
        return value
    if isinstance(value, t):
        return value
    raise ValueError(f"unexpected type of value from result "
                     f"(should be '{t.__name__}', got '{type(value).__name__}')"
                     )
