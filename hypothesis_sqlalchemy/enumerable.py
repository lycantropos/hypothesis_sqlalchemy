from enum import (Enum,
                  EnumMeta,
                  _is_dunder as is_ignored_key,
                  _is_sunder)
from typing import (Any,
                    Callable,
                    Dict,
                    Hashable,
                    Optional,
                    Sequence)

from hypothesis import strategies

from .hints import Strategy
from .utils import python_identifiers

Bases = Sequence[type]
UniqueBy = Optional[Callable[[Any], Hashable]]


def factory(*,
            names: Strategy[str] = python_identifiers,
            bases: Strategy[Bases] =
            strategies.tuples(strategies.just(Enum)),
            keys: Strategy[str],
            values: Strategy[Any] = strategies.integers(),
            unique_by: UniqueBy = None,
            min_size: int = 0,
            max_size: Optional[int] = None) -> Strategy:
    contents = (strategies.tuples(strategies.lists(keys,
                                                   min_size=min_size,
                                                   max_size=max_size,
                                                   unique=True),
                                  strategies.lists(values,
                                                   min_size=min_size,
                                                   max_size=max_size,
                                                   unique_by=unique_by))
                .map(lambda items: dict(zip(*items))))
    return (strategies.tuples(names, bases, contents)
            .map(lambda args: _to_enum(*args)))


def _to_enum(name: str, bases: Bases, contents: Dict[str, Any]) -> type:
    contents = _to_enum_contents(name, bases, contents)
    return EnumMeta(name, bases, contents)


def _to_enum_contents(name: str,
                      bases: Bases,
                      contents: Dict[str, Any]) -> Dict[str, Any]:
    result = EnumMeta.__prepare__(name, bases)
    # can't use `update` method because `_EnumDict` overloads `__setitem__`
    for name, content in contents.items():
        result[name] = content
    return result


def is_valid_key(key: str) -> bool:
    return not is_invalid_key(key) and not is_ignored_key(key)


def is_invalid_key(key: str) -> bool:
    return _is_sunder(key) or key == type.mro.__name__
