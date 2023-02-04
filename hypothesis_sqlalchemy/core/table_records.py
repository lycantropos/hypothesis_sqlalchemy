from typing import (Any,
                    List,
                    Optional)

from sqlalchemy.schema import Table

from . import columns_records
from .hints import (Record,
                    Scalar,
                    Strategy)


def instances(table: Table,
              **fixed_columns_values: Strategy[Scalar]) -> Strategy[Record]:
    return columns_records.instances(list(table.columns),
                                     **fixed_columns_values)


def lists(table: Table,
          *,
          min_size: int = 0,
          max_size: Optional[int] = None,
          **fixed_columns_values: Strategy[Any]
          ) -> Strategy[List[Record]]:
    return columns_records.lists(list(table.columns), table.constraints,
                                 min_size=min_size,
                                 max_size=max_size,
                                 **fixed_columns_values)
