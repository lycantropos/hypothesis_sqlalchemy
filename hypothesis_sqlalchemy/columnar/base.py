from operator import attrgetter
from typing import (Any,
                    Callable,
                    List,
                    Optional)

from hypothesis import strategies
from sqlalchemy.engine import Dialect
from sqlalchemy.schema import Column
from sqlalchemy.sql.type_api import TypeEngine

from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.utils import (is_column_unique,
                                         to_sql_identifiers)
from . import types as _types


def non_primary_keys_factory(
        dialect: Dialect,
        *,
        names: Optional[Strategy[str]] = None,
        types: Optional[Strategy[TypeEngine]] = None,
        are_unique: Strategy[bool] = strategies.booleans(),
        are_nullable: Strategy[bool] = strategies.booleans(),
        are_indexed: Strategy[bool] = strategies.booleans()
) -> Strategy[Column]:
    if names is None:
        names = to_sql_identifiers(dialect)
    if types is None:
        types = _types.factory(dialect)
    return strategies.builds(Column,
                             name=names,
                             type_=types,
                             unique=are_unique,
                             nullable=are_nullable,
                             primary_key=strategies.just(False),
                             index=are_indexed)


def primary_keys_factory(
        dialect: Dialect,
        *,
        names: Optional[Strategy[str]] = None,
        types: Optional[Strategy[TypeEngine]] = None,
        are_auto_incremented: Strategy[bool] = strategies.just(True)
) -> Strategy:
    if names is None:
        names = to_sql_identifiers(dialect)
    if types is None:
        types = _types.factory(dialect)
    return strategies.builds(Column,
                             name=names,
                             type_=types,
                             autoincrement=are_auto_incremented,
                             primary_key=strategies.just(True))


def lists_factory(
        dialect: Dialect,
        *,
        primary_keys: Optional[Strategy[str]] = None,
        non_primary_keys: Optional[Strategy[TypeEngine]] = None,
        min_size: int = 0,
        max_size: Optional[int] = None) -> Strategy[List[Column]]:
    if primary_keys is None:
        primary_keys = primary_keys_factory(dialect)
    if non_primary_keys is None:
        non_primary_keys = non_primary_keys_factory(dialect)
    min_size = min_size - 1 if min_size > 0 else min_size
    max_size = max_size - 1 if max_size is not None else max_size
    rest_columns_lists = strategies.lists(non_primary_keys,
                                          min_size=min_size,
                                          max_size=max_size,
                                          unique_by=attrgetter('name'))

    def to_columns_lists(draw: Callable[[Strategy], Any]) -> List[Column]:
        primary_key = draw(primary_keys)

        def names_are_unique(columns: List[Column]) -> bool:
            names = [primary_key.name] + [column.name for column in columns]
            return len(names) == len(set(names))

        rest_columns_list = draw(rest_columns_lists
                                 .filter(names_are_unique))
        return [primary_key] + rest_columns_list

    return strategies.composite(to_columns_lists)()


def non_all_unique_lists_factory(dialect: Dialect,
                                 *,
                                 min_size: int = 0,
                                 max_size: Optional[int] = None
                                 ) -> Strategy[List[Column]]:
    def has_non_unique_column(columns: List[Column]) -> bool:
        return not all(is_column_unique(column)
                       for column in columns)

    return (lists_factory(dialect,
                          min_size=min_size,
                          max_size=max_size)
            .filter(has_non_unique_column))
