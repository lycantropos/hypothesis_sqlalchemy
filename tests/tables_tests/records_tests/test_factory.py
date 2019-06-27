from typing import (Any,
                    Dict,
                    Tuple)

from hypothesis import given
from sqlalchemy.schema import Table

from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.tables.records import factory
from tests.utils import (DataObject,
                         table_record_is_valid)
from . import strategies


@given(strategies.tables_with_fixed_columns_values)
def test_basic(table_fixed_columns_values: Tuple[Table,
                                                 Dict[str, Strategy[Any]]]
               ) -> None:
    table, fixed_columns_values = table_fixed_columns_values

    result = factory(table, **fixed_columns_values)

    assert isinstance(result, Strategy)


@given(strategies.data, strategies.tables_with_fixed_columns_values)
def test_examples(data: DataObject,
                  table_fixed_columns_values: Tuple[Table,
                                                    Dict[str, Strategy[Any]]]
                  ) -> None:
    table, fixed_columns_values = table_fixed_columns_values

    strategy = factory(table, **fixed_columns_values)

    result = data.draw(strategy)

    assert isinstance(result, tuple)
    assert table_record_is_valid(result,
                                 table=table)
