from typing import Any

from hypothesis import strategies
from sqlalchemy.engine import Dialect
from sqlalchemy.schema import Column

from . import column_type
from .hints import Scalar, Strategy
from .utils import to_sql_identifiers


def instances(
    dialect: Dialect,
    *,
    names: Strategy[str] | None = None,
    types: Strategy[column_type.TypeOrInstance] | None = None,
    are_unique: Strategy[bool | None] = strategies.none(),  # ruff: ignore[function-call-in-default-argument]
    are_primary_keys: Strategy[bool | None] = strategies.none(),  # ruff: ignore[function-call-in-default-argument]
    are_auto_incremented: Strategy[bool | None] = strategies.none(),  # ruff: ignore[function-call-in-default-argument]
    are_nullable: Strategy[bool | None] = strategies.booleans(),  # ruff: ignore[function-call-in-default-argument]
    are_indexed: Strategy[bool | None] = strategies.booleans(),  # ruff: ignore[function-call-in-default-argument]
) -> Strategy[Column[Any]]:
    names = to_sql_identifiers(dialect) if names is None else names
    types = column_type.instances(dialect) if types is None else types
    return strategies.builds(
        Column,
        name=names,
        type_=types,
        autoincrement=are_auto_incremented,
        unique=are_unique,
        nullable=are_nullable,
        primary_key=are_primary_keys,
        index=are_indexed,
    )


def scalars(column: Column[Scalar]) -> Strategy[Scalar]:
    result = column_type.scalars(column.type)
    return strategies.none() | result if column.nullable else result
