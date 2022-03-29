from typing import (Optional,
                    Tuple)

from hypothesis import given
from sqlalchemy.engine import Dialect
from sqlalchemy.schema import (MetaData,
                               Table)

import hypothesis_sqlalchemy.scheme as relational
from hypothesis_sqlalchemy.core.hints import Strategy
from tests.utils import DataObject
from . import strategies


@given(strategies.dialects, strategies.min_tables_sizes,
       strategies.max_tables_sizes)
def test_basic(dialect: Dialect,
               min_size: int,
               max_size: Optional[int]) -> None:
    result = relational.tables(dialect=dialect,
                               metadatas=strategies.metadatas,
                               min_size=min_size,
                               max_size=max_size)

    assert isinstance(result, Strategy)


@given(strategies.data, strategies.dialects, strategies.min_tables_sizes,
       strategies.max_tables_sizes)
def test_examples(data: DataObject,
                  dialect: Dialect,
                  min_size: int,
                  max_size: Optional[int]) -> None:
    strategy = relational.tables(dialect=dialect,
                                 metadatas=strategies.metadatas,
                                 min_size=min_size,
                                 max_size=max_size)

    result = data.draw(strategy)

    assert isinstance(result, Table)
    assert min_size <= len(result.columns)
    assert max_size is None or len(result.columns) <= max_size
    assert not result.columns or result.primary_key


@given(strategies.data, strategies.metadatas, strategies.dialects_with_names,
       strategies.min_tables_sizes, strategies.max_tables_sizes)
def test_extending(data: DataObject,
                   metadata: MetaData,
                   dialect_with_name: Tuple[Dialect, str],
                   min_size: int,
                   max_size: Optional[int]) -> None:
    dialect, name = dialect_with_name

    strategy = relational.tables(dialect=dialect,
                                 metadatas=strategies.just(metadata),
                                 names=strategies.just(name),
                                 min_size=min_size,
                                 max_size=max_size,
                                 extend_existing=strategies.just(True))

    first_result = data.draw(strategy)
    second_result = data.draw(strategy)

    assert first_result == second_result
