from typing import Optional

from hypothesis import given
from sqlalchemy.engine import Dialect
from sqlalchemy.schema import (MetaData,
                               Table)

from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.tabular import factory
from hypothesis_sqlalchemy.utils import is_column_unique
from tests.utils import DataObject
from . import strategies


@given(strategies.dialects,
       strategies.metadatas,
       strategies.min_sizes, strategies.max_sizes)
def test_basic(dialect: Dialect,
               metadata: MetaData,
               min_size: int,
               max_size: Optional[int]) -> None:
    result = factory(dialect=dialect,
                     metadata=metadata,
                     min_size=min_size,
                     max_size=max_size)

    assert isinstance(result, Strategy)


@given(strategies.data, strategies.dialects,
       strategies.metadatas,
       strategies.min_sizes, strategies.max_sizes)
def test_examples(data: DataObject,
                  dialect: Dialect,
                  metadata: MetaData,
                  min_size: int,
                  max_size: Optional[int]) -> None:
    strategy = factory(dialect=dialect,
                       metadata=metadata,
                       min_size=min_size,
                       max_size=max_size)

    result = data.draw(strategy)

    assert isinstance(result, Table)
    assert min_size <= len(result.columns)
    assert max_size is None or len(result.columns) <= max_size
    assert not all(map(is_column_unique, result.columns))
