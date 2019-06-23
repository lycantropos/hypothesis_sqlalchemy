from enum import (Enum,
                  EnumMeta,
                  IntEnum)
from itertools import filterfalse
from typing import (Any,
                    Tuple)

from hypothesis import strategies
from hypothesis.searchstrategy import SearchStrategy

from hypothesis_sqlalchemy.enums import (Bases,
                                         UniqueBy,
                                         is_invalid_enum_key)
from tests.strategies import (data,
                              max_sizes,
                              min_sizes)

data = data
max_sizes = max_sizes
min_sizes = min_sizes
integers = strategies.integers()
floats = strategies.floats()
strings = strategies.text()
scalars = (strategies.builds(object)
           | strategies.none()
           | integers
           | strings
           | floats
           | strategies.datetimes())
invalid_keys_types_strategies = strategies.just(strategies.none())
invalid_keys_values_strategies = strategies.just(strings
                                                 .map('_{}_'.format)
                                                 .filter(is_invalid_enum_key))

_non_enum_bases = [str, float, int]
_valid_class_strategies = {str: scalars,
                           float: floats | floats.map(str),
                           int: integers | integers.map(str)}


class _NoStrConvertible:
    __str__ = __repr__ = None


_invalid_class_strategies = {str: strategies.builds(_NoStrConvertible),
                             float: strategies.none(),
                             int: strategies.none()}


def is_enum_class(cls: type) -> bool:
    return isinstance(cls, EnumMeta)


def combine_bases_with_values(bases: Bases) -> Tuple[SearchStrategy[Bases],
                                                     SearchStrategy[Any]]:
    if any(base is IntEnum for base in bases):
        values = _valid_class_strategies[int]
    else:
        try:
            non_enum_base = next(filterfalse(is_enum_class, bases))
        except StopIteration:
            values = scalars
        else:
            values = _valid_class_strategies[non_enum_base]
    return strategies.just(bases), values


def combine_bases_with_unique_values(bases: Bases
                                     ) -> Tuple[SearchStrategy[Bases],
                                                SearchStrategy[Any],
                                                UniqueBy]:
    if any(base is IntEnum for base in bases):
        values = _valid_class_strategies[int]
        unique_by = int
    else:
        try:
            non_enum_base = next(filterfalse(is_enum_class, bases))
        except StopIteration:
            values = scalars
            unique_by = lambda x: x
        else:
            values = _valid_class_strategies[non_enum_base]
            unique_by = non_enum_base
    return strategies.just(bases), values, unique_by


def combine_bases_with_invalid_values(bases: Bases
                                      ) -> Tuple[SearchStrategy[Bases],
                                                 SearchStrategy[Any]]:
    if any(base is IntEnum for base in bases):
        values = _invalid_class_strategies[int]
    else:
        try:
            non_enum_base = next(filterfalse(is_enum_class, bases))
        except StopIteration:
            raise ValueError('Can\'t produce invalid values '
                             'for generic enum class.')
        values = _invalid_class_strategies[non_enum_base]
    return strategies.just(bases), values


plain_bases = strategies.tuples(strategies.just(Enum))
complex_bases = (strategies.tuples(strategies.just(IntEnum)) |
                 strategies.tuples(strategies.sampled_from(_non_enum_bases),
                                   strategies.just(Enum)))
bases_values_strategies = ((plain_bases | complex_bases)
                           .map(combine_bases_with_values))
bases_unique_values_strategies = ((plain_bases | complex_bases)
                                  .map(combine_bases_with_unique_values))
bases_invalid_values_strategies = complex_bases.map(
        combine_bases_with_invalid_values)
