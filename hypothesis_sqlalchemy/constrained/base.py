from operator import add
from typing import (List,
                    Optional)

from hypothesis import strategies
from sqlalchemy import (Constraint,
                        PrimaryKeyConstraint,
                        UniqueConstraint)
from sqlalchemy.schema import Column

from hypothesis_sqlalchemy.hints import Strategy

UNIQUE_TYPES = (PrimaryKeyConstraint, UniqueConstraint)


def lists_factory(columns: List[Column],
                  *,
                  min_size: int = 0,
                  max_size: Optional[int] = None
                  ) -> Strategy[List[Constraint]]:
    if not columns:
        return strategies.builds(list)
    primary_keys_lists = primary_keys_factory(columns).map(lambda key: [key])
    return (strategies.tuples(primary_keys_lists,
                              strategies.lists(unique_factory(columns),
                                               min_size=max(min_size - 1, 0),
                                               max_size=max_size - 1
                                               if max_size is not None
                                               else max_size))
            .map(lambda lists_pair: add(*lists_pair)))


def unique_factory(columns: List[Column]) -> Strategy[UniqueConstraint]:
    return (strategies.sets(strategies.sampled_from(columns) if columns
                            else strategies.nothing(),
                            max_size=len(columns))
            .map(lambda constraint_columns:
                 UniqueConstraint(*constraint_columns)))


def primary_keys_factory(columns: List[Column],
                         *,
                         min_size: int = 1) -> Strategy[PrimaryKeyConstraint]:
    if not columns:
        raise ValueError('`columns` should not be empty')
    if min_size < 1:
        raise ValueError('`min_size` should be at least 1')
    existing_columns = [column for column in columns if column.primary_key]
    if existing_columns:
        return strategies.just(PrimaryKeyConstraint(*existing_columns))
    return (strategies.sets(strategies.sampled_from(columns),
                            min_size=min_size,
                            max_size=len(columns))
            .map(lambda constraint_columns:
                 PrimaryKeyConstraint(*constraint_columns)))
