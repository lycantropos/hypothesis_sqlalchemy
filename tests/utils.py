from collections.abc import Hashable, Iterable
from typing import Any
from uuid import UUID

from hypothesis import strategies as st
from sqlalchemy import Column, Table
from sqlalchemy.dialects import postgresql

from hypothesis_sqlalchemy.core import table_constraints
from hypothesis_sqlalchemy.hints import Record

Bounds = tuple[int, int | None]
DataObject = st.DataObject

MAX_SIZE = 100
MAX_MIN_SIZE = MAX_SIZE // 2


def table_record_is_valid(table_record: Record, *, table: Table) -> bool:
    return all(
        (coordinate is None and column.nullable)
        or isinstance(coordinate, to_python_type(column))
        for coordinate, column in zip(table_record, table.columns, strict=True)
    )


def to_python_type(column: Column[Any]) -> type[Any]:
    column_type = column.type
    if isinstance(column_type, postgresql.UUID):
        return UUID if column_type.as_uuid else str
    return column_type.python_type


def records_satisfy_table_constraints(
    records: list[Record], *, table: Table
) -> bool:
    def all_unique(iterable: Iterable[Hashable]) -> bool:
        seen = set()
        for element in iterable:
            if element in seen:
                return False
            seen.add(element)
        return True

    columns_indices = {
        column: index for index, column in enumerate(table.columns)
    }
    return all(
        all_unique(
            tuple(
                record[columns_indices[column]]
                for column in constraint.columns
            )
            for record in records
        )
        for constraint in table.constraints
        if isinstance(constraint, table_constraints.UNIQUE_TYPES)
        and constraint.columns
    )
