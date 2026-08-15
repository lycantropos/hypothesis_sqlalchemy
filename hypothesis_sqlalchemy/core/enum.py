from collections.abc import Callable, Hashable, Iterable, Mapping
from enum import Enum, EnumMeta
from typing import Any

from hypothesis import strategies as st

from .hints import Strategy
from .utils import python_identifiers

Bases = tuple[type[Any], ...]
Contents = Mapping[str, Any]
UniqueBy = Callable[[Any], Hashable] | None


def types(
    *,
    names: Strategy[str] = python_identifiers,
    bases: Strategy[Bases] = st.tuples(  # ruff: ignore[function-call-in-default-argument]
        st.just(Enum)  # ruff: ignore[function-call-in-default-argument]
    ),
    keys: Strategy[str],
    values: Strategy[Any] = st.integers(),  # ruff: ignore[function-call-in-default-argument]
    unique_by: UniqueBy = None,
    min_size: int = 0,
    max_size: int | None = None,
    _to_contents: Callable[
        [Iterable[str], Iterable[Any]], Contents
    ] = lambda keys, values: dict(zip(keys, values, strict=False)),
) -> Strategy[EnumMeta]:
    contents = st.builds(
        _to_contents,
        st.lists(keys, min_size=min_size, max_size=max_size, unique=True),
        st.lists(
            values, min_size=min_size, max_size=max_size, unique_by=unique_by
        ),
    )
    return st.builds(_to_enum, names, bases, contents)


def _to_enum(name: str, bases: Bases, contents: Contents) -> EnumMeta:
    return EnumMeta(name, bases, _to_enum_contents(name, bases, contents))  # pyright: ignore[reportReturnType]


def _to_enum_contents(
    name: str, bases: Bases, contents: Mapping[str, Any]
) -> Any:
    result = EnumMeta.__prepare__(name, bases)
    # can't use `update` method because `_EnumDict` overloads `__setitem__`
    for name, content in contents.items():
        result[name] = content
    return result


def is_valid_key(key: str) -> bool:
    return not is_invalid_key(key) and not _is_dunder(key)


def is_invalid_key(key: str) -> bool:
    return _is_sunder(key) or key == type.mro.__name__


def _is_dunder(name: str) -> bool:
    """Checks whether name has ``__dunder__`` form."""
    return (
        len(name) > 4
        and name[:2] == name[-2:] == '__'
        and name[2] != '_'
        and name[-3] != '_'
    )


def _is_sunder(name: str) -> bool:
    """Checks whether name has ``_sunder_`` form."""
    return (
        len(name) > 2
        and name[0] == name[-1] == '_'
        and name[1:2] != '_'
        and name[-2:-1] != '_'
    )
