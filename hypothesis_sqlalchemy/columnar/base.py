from operator import attrgetter
from typing import (List,
                    Optional)

from hypothesis import strategies
from sqlalchemy.engine import Dialect
from sqlalchemy.schema import Column

from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.utils import to_sql_identifiers
from . import types as _types


def factory(dialect: Dialect,
            *,
            names: Optional[Strategy[str]] = None,
            types: Optional[Strategy[_types.TypeOrInstance]] = None,
            are_unique: Strategy[Optional[bool]] = strategies.none(),
            are_primary_keys: Strategy[Optional[bool]] = strategies.none(),
            are_auto_incremented: Strategy[Optional[bool]] = strategies.none(),
            are_nullable: Strategy[Optional[bool]] = strategies.booleans(),
            are_indexed: Strategy[Optional[bool]] = strategies.booleans()
            ) -> Strategy[Column]:
    names = to_sql_identifiers(dialect) if names is None else names
    types = _types.factory(dialect) if types is None else types
    return strategies.builds(Column,
                             name=names,
                             type_=types,
                             autoincrement=are_auto_incremented,
                             unique=are_unique,
                             nullable=are_nullable,
                             primary_key=are_primary_keys,
                             index=are_indexed)


def lists_factory(columns: Strategy[Column],
                  *,
                  min_size: int = 0,
                  max_size: Optional[int] = None) -> Strategy[List[Column]]:
    return strategies.lists(columns,
                            min_size=min_size,
                            max_size=max_size,
                            unique_by=attrgetter('name'))
