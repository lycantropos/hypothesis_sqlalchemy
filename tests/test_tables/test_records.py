from functools import partial

from hypothesis.searchstrategy import SearchStrategy
from sqlalchemy.schema import Table

from hypothesis_sqlalchemy.tables import records
from tests.utils import (example,
                         table_record_is_valid)


def test_table_records_factory(table: Table) -> None:
    table_records_strategy = records.factory(table)
    table_record = example(table_records_strategy)

    assert isinstance(table_records_strategy, SearchStrategy)
    assert isinstance(table_record, tuple)
    assert table_record_is_valid(table_record,
                                 table=table)


def test_table_records_lists_factory(table: Table) -> None:
    table_records_lists = records.lists_factory(table)
    table_records = example(table_records_lists)

    assert isinstance(table_records_lists, SearchStrategy)
    assert isinstance(table_records, list)
    assert all(isinstance(record, tuple)
               for record in table_records)
    assert all(map(partial(table_record_is_valid,
                           table=table),
                   table_records))
