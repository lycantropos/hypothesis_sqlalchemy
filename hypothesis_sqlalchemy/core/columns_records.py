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
from .column import scalars as column_values
from .hints import (Record,
                    Strategy)


def instances(columns: List[Column],
              **fixed_columns_values: Strategy[Any]) -> Strategy[Record]:
    def to_plain_values_strategy(column: Column) -> Strategy[Any]:
        result = column_values(column)
        if column.nullable:
            # putting simpler strategies first
            # more info at
            # https://hypothesis.readthedocs.io/en/latest/data.html#hypothesis.strategies.one_of
            result = strategies.none() | result
        return result

    if fixed_columns_values:
        def to_values_strategy(column: Column) -> Strategy[Any]:
            column_name = column.name
            if column_name in fixed_columns_values:
                return fixed_columns_values[column_name]
            else:
                return to_plain_values_strategy(column)
    else:
        to_values_strategy = to_plain_values_strategy
    return strategies.tuples(*map(to_values_strategy, columns))


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
