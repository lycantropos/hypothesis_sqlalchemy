from typing import Dict

from hypothesis.searchstrategy.collections import TupleStrategy
from sqlalchemy import Table

from hypothesis_sqlalchemy import records
from hypothesis_sqlalchemy.types import Strategy
from hypothesis_sqlalchemy.utils import (MIN_RECORDS_COUNT,
                                         MAX_RECORDS_COUNT)


def factory(table: Table,
            **fixed_columns_values: Dict[str, Strategy]
            ) -> TupleStrategy:
    return records.factory(table.columns,
                           **fixed_columns_values)


def lists_factory(table: Table,
                  min_size: int = MIN_RECORDS_COUNT,
                  max_size: int = MAX_RECORDS_COUNT,
                  **fixed_columns_values: Dict[str, Strategy]
                  ) -> TupleStrategy:
    return records.lists_factory(table.columns,
                                 min_size=min_size,
                                 max_size=max_size,
                                 **fixed_columns_values)
