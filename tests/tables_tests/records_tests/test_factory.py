from hypothesis import given
from hypothesis.searchstrategy import SearchStrategy
from sqlalchemy.schema import Table

from hypothesis_sqlalchemy.tables.records import factory
from tests.utils import (DataObject,
                         table_record_is_valid)
from . import strategies


@given(strategies.tables)
def test_basic(table: Table) -> None:
    result = factory(table)

    assert isinstance(result, SearchStrategy)


@given(strategies.data, strategies.tables)
def test_examples(data: DataObject, table: Table) -> None:
    strategy = factory(table)

    result = data.draw(strategy)

    assert isinstance(result, tuple)
    assert table_record_is_valid(result,
                                 table=table)
