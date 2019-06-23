from functools import partial
from typing import Optional

from hypothesis import given
from hypothesis.searchstrategy import SearchStrategy
from hypothesis.strategies import DataObject
from sqlalchemy.schema import Table

from hypothesis_sqlalchemy.tables.records import lists_factory
from tests import strategies
from tests.utils import table_record_is_valid


@given(strategies.tables, strategies.min_sizes, strategies.max_sizes)
def test_basic(table: Table, min_size: int, max_size: Optional[int]) -> None:
    result = lists_factory(table,
                           min_size=min_size,
                           max_size=max_size)

    assert isinstance(result, SearchStrategy)


@given(strategies.data, strategies.tables,
       strategies.min_sizes, strategies.max_sizes)
def test_lists_factory(data: DataObject,
                       table: Table,
                       min_size: int,
                       max_size: Optional[int]) -> None:
    strategy = lists_factory(table,
                             min_size=min_size,
                             max_size=max_size)

    result = data.draw(strategy)

    assert isinstance(strategy, SearchStrategy)
    assert isinstance(result, list)
    assert min_size <= len(result)
    assert max_size is None or len(result) <= max_size
    assert all(isinstance(record, tuple)
               for record in result)
    assert all(map(partial(table_record_is_valid,
                           table=table),
                   result))
