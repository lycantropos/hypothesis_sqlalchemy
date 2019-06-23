from typing import Optional

from hypothesis.searchstrategy.collections import TupleStrategy
from sqlalchemy import Table

from hypothesis_sqlalchemy import columns
from hypothesis_sqlalchemy.hints import Strategy


def factory(table: Table,
            **fixed_columns_values: Strategy) -> TupleStrategy:
    return columns.records.factory(table.columns,
                                   **fixed_columns_values)


def lists_factory(table: Table,
                  *,
                  min_size: int = 0,
                  max_size: Optional[int] = None,
                  **fixed_columns_values: Strategy) -> TupleStrategy:
    return columns.records.lists_factory(table.columns,
                                         min_size=min_size,
                                         max_size=max_size,
                                         **fixed_columns_values)
