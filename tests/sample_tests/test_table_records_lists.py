from functools import partial
from typing import (Any,
                    Dict,
                    Optional,
                    Tuple)

from hypothesis import given
from sqlalchemy.schema import Table

from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.sample import table_records_lists
from tests.utils import (DataObject,
                         records_satisfy_table_constraints,
                         table_record_is_valid)
from . import strategies


@given(strategies.tables_with_fixed_columns_values,
       strategies.min_table_records_lists_sizes,
       strategies.max_table_records_lists_sizes)
def test_basic(table_fixed_columns_values: Tuple[Table,
                                                 Dict[str, Strategy[Any]]],
               min_size: int, max_size: Optional[int]) -> None:
    table, fixed_columns_values = table_fixed_columns_values

    result = table_records_lists(table,
                                 min_size=min_size,
                                 max_size=max_size,
                                 **fixed_columns_values)

    assert isinstance(result, Strategy)


@given(strategies.data, strategies.tables_with_fixed_columns_values,
       strategies.min_table_records_lists_sizes,
       strategies.max_table_records_lists_sizes)
def test_lists_factory(data: DataObject,
                       table_fixed_columns_values
                       : Tuple[Table, Dict[str, Strategy[Any]]],
                       min_size: int,
                       max_size: Optional[int]) -> None:
    table, fixed_columns_values = table_fixed_columns_values

    strategy = table_records_lists(table,
                                   min_size=min_size,
                                   max_size=max_size,
                                   **fixed_columns_values)

    result = data.draw(strategy)

    assert isinstance(result, list)
    assert min_size <= len(result)
    assert max_size is None or len(result) <= max_size
    assert all(isinstance(record, tuple)
               for record in result)
    assert all(map(partial(table_record_is_valid,
                           table=table),
                   result))
    assert records_satisfy_table_constraints(result,
                                             table=table)
