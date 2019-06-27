from enum import EnumMeta
from typing import (Any,
                    Optional,
                    Tuple)

import pytest
from hypothesis import given
from hypothesis.searchstrategy import SearchStrategy

from hypothesis_sqlalchemy.enums import (Bases,
                                         UniqueBy,
                                         factory)
from tests.utils import DataObject
from . import strategies


@given(strategies.bases_values_strategies, strategies.min_sizes,
       strategies.keys_strategies, strategies.max_sizes)
def test_basic(bases_values: Tuple[SearchStrategy[strategies.Bases],
                                   SearchStrategy[Any]],
               keys: SearchStrategy[str],
               min_size: int,
               max_size: Optional[int]) -> None:
    bases, values = bases_values

    result = factory(bases=bases,
                     keys=keys,
                     values=values,
                     min_size=min_size,
                     max_size=max_size)

    assert isinstance(result, SearchStrategy)


@given(strategies.data, strategies.bases_values_strategies,
       strategies.keys_strategies, strategies.min_sizes, strategies.max_sizes)
def test_example(data: DataObject,
                 bases_values: Tuple[SearchStrategy[strategies.Bases],
                                     SearchStrategy[Any]],
                 keys: SearchStrategy[str],
                 min_size: int,
                 max_size: Optional[int]) -> None:
    bases, values = bases_values
    strategy = factory(bases=bases,
                       keys=keys,
                       values=values,
                       min_size=min_size,
                       max_size=max_size)

    result = data.draw(strategy)

    assert isinstance(result, EnumMeta)
    # not checking `len` because of aliases
    assert min_size <= len(result.__members__)
    assert max_size is None or len(result.__members__) <= max_size


@given(strategies.data, strategies.bases_unique_values_strategies,
       strategies.keys_strategies, strategies.min_sizes, strategies.max_sizes)
def test_unique_by(data: DataObject,
                   bases_values_unique_by: Tuple[SearchStrategy[Bases],
                                                 SearchStrategy[Any],
                                                 UniqueBy],
                   keys: SearchStrategy[str],
                   min_size: int,
                   max_size: Optional[int]) -> None:
    bases, values, unique_by = bases_values_unique_by
    strategy = factory(bases=bases,
                       keys=keys,
                       values=values,
                       min_size=min_size,
                       max_size=max_size,
                       unique_by=unique_by)

    result = data.draw(strategy)

    assert isinstance(result, EnumMeta)
    assert min_size <= len(result)
    assert max_size is None or len(result) <= max_size


@given(strategies.data, strategies.invalid_keys_types_strategies)
def test_invalid_keys_types(data: DataObject,
                            keys: SearchStrategy[Any]) -> None:
    strategy = factory(keys=keys,
                       min_size=1)

    with pytest.raises(TypeError):
        data.draw(strategy)


@given(strategies.data, strategies.invalid_keys_values_strategies)
def test_invalid_keys_values(data: DataObject,
                             keys: SearchStrategy[str]) -> None:
    strategy = factory(keys=keys,
                       min_size=1)

    with pytest.raises(ValueError):
        data.draw(strategy)


@given(strategies.data, strategies.bases_invalid_values_strategies,
       strategies.keys_strategies)
def test_invalid_values(data: DataObject,
                        bases_invalid_values: Tuple[SearchStrategy[Bases],
                                                    SearchStrategy[Any]],
                        keys: SearchStrategy[str]) -> None:
    bases, invalid_values = bases_invalid_values

    result = factory(bases=bases,
                     keys=keys,
                     values=invalid_values,
                     min_size=1)

    with pytest.raises(TypeError):
        data.draw(result)
