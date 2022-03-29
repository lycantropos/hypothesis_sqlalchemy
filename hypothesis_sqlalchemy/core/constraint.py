from typing import Optional

from hypothesis import strategies
from sqlalchemy.schema import (PrimaryKeyConstraint,
                               Table,
                               UniqueConstraint)

from .hints import Strategy


def unique(table: Table,
           *,
           min_size: int = 0,
           max_size: Optional[int] = None) -> Strategy[UniqueConstraint]:
    if max_size is None:
        max_size = len(table.columns)
    return (strategies.sets(strategies.sampled_from(table.columns)
                            if table.columns
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
    existing_columns = [column
                        for column in table.columns
                        if column.primary_key]
    if existing_columns:
        return strategies.just(PrimaryKeyConstraint(*existing_columns))
    return (strategies.sets(strategies.sampled_from(table.columns)
                            if table.columns
                            else strategies.nothing(),
                            min_size=min_size,
                            max_size=max_size)
            .map(lambda constraint_columns:
                 PrimaryKeyConstraint(*constraint_columns)))
