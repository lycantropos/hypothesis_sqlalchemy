from itertools import starmap
from operator import itemgetter
from typing import (AbstractSet,
                    Any,
                    List,
                    Optional)

from hypothesis import strategies
from sqlalchemy.schema import (Column,
                               Constraint)

from . import table_constraints
from .column import scalars
from .hints import (Record,
                    Scalar,
                    Strategy)


def instances(columns: List[Column],
              **fixed_columns_values: Strategy[Scalar]) -> Strategy[Record]:
    if fixed_columns_values:
        def column_scalars(column: Column) -> Strategy[Scalar]:
            column_name = column.name
            return (fixed_columns_values[column_name]
                    if column_name in fixed_columns_values
                    else scalars(column))
    else:
        column_scalars = scalars
    return strategies.tuples(*map(column_scalars, columns))


def lists(columns: List[Column],
          constraints: AbstractSet[Constraint],
          *,
          min_size: int = 0,
          max_size: Optional[int] = None,
          **fixed_columns_values: Strategy[Any]) -> Strategy[List[Record]]:
    columns_indices = {column: index for index, column in enumerate(columns)}
    unique_indices = [[columns_indices[column]
                       for column in constraint.columns]
                      for constraint in constraints
                      if isinstance(constraint, table_constraints.UNIQUE_TYPES)
                      and constraint.columns]
    unique_by = (tuple(starmap(itemgetter, unique_indices))
                 if unique_indices
                 else None)
    return strategies.lists(instances(columns, **fixed_columns_values),
                            min_size=min_size,
                            max_size=max_size,
                            unique_by=unique_by)
