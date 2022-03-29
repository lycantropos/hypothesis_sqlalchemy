from operator import add
from typing import (List,
                    Optional)

from hypothesis import strategies
from sqlalchemy.schema import (Constraint,
                               PrimaryKeyConstraint,
                               Table,
                               UniqueConstraint)

from .hints import Strategy

UNIQUE_TYPES = (PrimaryKeyConstraint, UniqueConstraint)


def unique(table: Table,
           *,
           min_size: int = 0,
           max_size: Optional[int] = None) -> Strategy[UniqueConstraint]:
    columns = list(table.columns)
    if max_size is None:
        max_size = len(columns)
    return (strategies.sets(strategies.sampled_from(columns)
                            if columns
                            else strategies.nothing(),
                            min_size=min_size,
                            max_size=max_size)
            .map(lambda constraint_columns:
                 UniqueConstraint(*constraint_columns)))


def primary_keys(table: Table,
                 *,
                 min_size: int = 0,
                 max_size: Optional[int] = None
                 ) -> Strategy[PrimaryKeyConstraint]:
    columns = list(table.columns)
    existing_columns = [column for column in columns if column.primary_key]
    if existing_columns:
        return strategies.just(PrimaryKeyConstraint(*existing_columns))
    return (strategies.sets(strategies.sampled_from(columns)
                            if columns
                            else strategies.nothing(),
                            min_size=min_size,
                            max_size=max_size)
            .map(lambda constraint_columns:
                 PrimaryKeyConstraint(*constraint_columns)))


def lists(table: Table,
          *,
          min_size: int = 0,
          max_size: Optional[int] = None,
          primary_key_min_size: int = 0,
          primary_key_max_size: Optional[int] = None,
          unique_min_size: int = 0,
          unique_max_size: Optional[int] = None) -> Strategy[List[Constraint]]:
    if not table.columns:
        return strategies.builds(list)
    primary_keys_lists = (primary_keys(table,
                                       min_size=primary_key_min_size,
                                       max_size=primary_key_max_size)
                          .map(lambda key: [key]))
    unique_lists = strategies.lists(unique(table,
                                           min_size=unique_min_size,
                                           max_size=unique_max_size),
                                    min_size=max(min_size - 1, 0),
                                    max_size=max_size - 1
                                    if max_size is not None
                                    else max_size)
    return (strategies.tuples(primary_keys_lists, unique_lists)
            .map(lambda lists_pair: add(*lists_pair)))
