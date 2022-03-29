from typing import Optional

from hypothesis import strategies
from sqlalchemy.engine import Dialect
from sqlalchemy.schema import Column

from . import column_type
from .hints import (Scalar,
                    Strategy)
from .utils import to_sql_identifiers


def instances(dialect: Dialect,
              *,
              names: Optional[Strategy[str]] = None,
              types: Optional[Strategy[column_type.TypeOrInstance]] = None,
              are_unique: Strategy[Optional[bool]] = strategies.none(),
              are_primary_keys: Strategy[Optional[bool]] = strategies.none(),
              are_auto_incremented: Strategy[Optional[bool]]
              = strategies.none(),
              are_nullable: Strategy[Optional[bool]] = strategies.booleans(),
              are_indexed: Strategy[Optional[bool]] = strategies.booleans()
              ) -> Strategy[Column]:
    names = to_sql_identifiers(dialect) if names is None else names
    types = column_type.instances(dialect) if types is None else types
    return strategies.builds(Column,
                             name=names,
                             type_=types,
                             autoincrement=are_auto_incremented,
                             unique=are_unique,
                             nullable=are_nullable,
                             primary_key=are_primary_keys,
                             index=are_indexed)


def scalars(column: Column) -> Strategy[Scalar]:
    result = column_type.scalars(column.type)
    return strategies.none() | result if column.nullable else result
