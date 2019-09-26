from itertools import starmap
from operator import itemgetter
from typing import (AbstractSet,
                    Any,
                    List,
                    Optional)

from hypothesis import strategies
from sqlalchemy.schema import (Column,
                               Constraint)

from hypothesis_sqlalchemy import constrained
from hypothesis_sqlalchemy.hints import (RecordType,
                                         Strategy)
from . import values


def factory(columns: List[Column],
            **fixed_columns_values: Strategy) -> Strategy[RecordType]:
    def to_plain_values_strategy(column: Column) -> Strategy[Any]:
        result = values.factory(column)
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


def lists_factory(columns: List[Column],
                  constraints: AbstractSet[Constraint],
                  *,
                  min_size: int = 0,
                  max_size: Optional[int] = None,
                  **fixed_columns_values: Strategy
                  ) -> Strategy[List[RecordType]]:
    values_tuples = factory(columns,
                            **fixed_columns_values)
    columns_indices = {column: index for index, column in enumerate(columns)}
    unique_indices = [[columns_indices[column]
                       for column in constraint.columns]
                      for constraint in constraints
                      if isinstance(constraint, constrained.UNIQUE_TYPES)
                      and constraint.columns]

    if unique_indices:
        # Create a tuple of functions, each function asserting the uniqueness
        # of a single column value
        unique_by = tuple(starmap(itemgetter, unique_indices))
    else:
        unique_by = None

    return strategies.lists(values_tuples,
                            min_size=min_size,
                            max_size=max_size,
                            unique_by=unique_by)
