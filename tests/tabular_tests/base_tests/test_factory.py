from typing import Optional

from hypothesis import given
from sqlalchemy.schema import (MetaData,
                               Table)

from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.tabular import factory
from hypothesis_sqlalchemy.utils import is_column_unique
from tests.utils import DataObject
from . import strategies


@given(strategies.metadatas_strategies,
       strategies.min_sizes, strategies.max_sizes)
def test_basic(metadatas: Strategy[MetaData],
               min_size: int,
               max_size: Optional[int]) -> None:
    result = factory(metadatas=metadatas,
                     min_size=min_size,
                     max_size=max_size)

    assert isinstance(result, Strategy)


@given(strategies.data, strategies.metadatas_strategies,
       strategies.min_sizes, strategies.max_sizes)
def test_examples(data: DataObject,
                  metadatas: Strategy[MetaData],
                  min_size: int,
                  max_size: Optional[int]) -> None:
    strategy = factory(metadatas=metadatas,
                       min_size=min_size,
                       max_size=max_size)

    result = data.draw(strategy)

    assert isinstance(result, Table)
    assert min_size <= len(result.columns)
    assert max_size is None or len(result.columns) <= max_size
    assert not all(map(is_column_unique, result.columns))
