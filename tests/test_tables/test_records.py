from functools import partial

from hypothesis.searchstrategy import SearchStrategy
from sqlalchemy.schema import (Column,
                               MetaData,
                               Table)
from sqlalchemy.sql.sqltypes import Integer

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
    _do_test_table_records_lists_factory(table, table_records_lists)


def test_table_records_lists_factory_for_table_without_primary_key() -> None:
    metadata = MetaData()
    table = Table('numbers', metadata, Column('number', Integer))
    # min_size = 2 is added as a regression test for a corner-case where the
    # absence of a primary key prevented multiple records from being generated:
    table_records_lists = records.lists_factory(table, min_size=2)
    _do_test_table_records_lists_factory(table, table_records_lists)


def _do_test_table_records_lists_factory(table: Table, table_records_lists: SearchStrategy) -> None:
    table_records = example(table_records_lists)

    assert isinstance(table_records_lists, SearchStrategy)
    assert isinstance(table_records, list)
    assert all(isinstance(record, tuple)
               for record in table_records)
    assert all(map(partial(table_record_is_valid,
                           table=table),
                   table_records))
