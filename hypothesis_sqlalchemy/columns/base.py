from typing import (Any,
                    Callable,
                    List,
                    Optional)

from hypothesis import strategies
from sqlalchemy.schema import Column
from sqlalchemy.sql.type_api import TypeEngine

from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.utils import (sql_identifiers,
                                         is_column_unique)
from . import types


def non_primary_keys_factory(
        *,
        names: Strategy[str] = sql_identifiers,
        types: Strategy[TypeEngine] = types.factory(),
        are_unique: Strategy[bool] = strategies.booleans(),
        are_nullable: Strategy[bool] = strategies.booleans(),
        are_indexed: Strategy[bool] = strategies.booleans()
) -> Strategy[Column]:
    return strategies.builds(Column,
                             name=names,
                             type_=types,
                             unique=are_unique,
                             nullable=are_nullable,
                             primary_key=strategies.just(False),
                             index=are_indexed)


def primary_keys_factory(
        *,
        names: Strategy[str] = sql_identifiers,
        types: Strategy[TypeEngine] = types.primary_keys_factory(),
        are_auto_incremented: Strategy[bool] = strategies.just(True)
) -> Strategy:
    return strategies.builds(Column,
                             name=names,
                             type_=types,
                             autoincrement=are_auto_incremented,
                             primary_key=strategies.just(True))


def lists_factory(
        *,
        primary_keys: Strategy[str] = primary_keys_factory(),
        non_primary_keys: Strategy[TypeEngine] = non_primary_keys_factory(),
        min_size: int = 0,
        max_size: Optional[int] = None) -> Strategy[List[Column]]:
    if min_size > 0:
        min_size -= 1
    if max_size is not None:
        max_size -= 1
    rest_columns_lists = strategies.lists(non_primary_keys,
                                          min_size=min_size,
                                          max_size=max_size)

    def to_columns_lists(draw: Callable[[Strategy], Any]) -> List[Column]:
        primary_key = draw(primary_keys)

        def names_are_unique(columns: List[Column]) -> bool:
            names = [primary_key.name]
            names += [column.name for column in columns]
            return len(names) == len(set(names))

        rest_columns_list = draw(rest_columns_lists
                                 .filter(names_are_unique))
        return [primary_key] + rest_columns_list

    return strategies.composite(to_columns_lists)()


def non_all_unique_lists_factory(
        min_size: int = 0,
        max_size: Optional[int] = None
) -> Strategy:
    def has_non_unique_column(columns: List[Column]) -> bool:
        return any(not is_column_unique(column)
                   for column in columns)

    return (lists_factory(min_size=min_size,
                          max_size=max_size)
            .filter(has_non_unique_column))
