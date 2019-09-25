from typing import (Hashable,
                    Iterable,
                    List)
from uuid import UUID

from sqlalchemy import (Column,
                        Table)
from sqlalchemy.dialects import postgresql

from hypothesis_sqlalchemy.hints import RecordType
from hypothesis_sqlalchemy.utils import is_column_unique

try:
    from hypothesis.strategies import DataObject
except ImportError:
    from hypothesis._strategies import DataObject

DataObject = DataObject


def table_record_is_valid(table_record: RecordType,
                          *,
                          table: Table) -> bool:
    return all(coordinate is None
               and column.nullable
               or isinstance(coordinate, to_python_type(column))
               for coordinate, column in zip(table_record, table.columns))


def to_python_type(column: Column) -> type:
    column_type = column.type
    if isinstance(column_type, postgresql.UUID):
        return UUID if column_type.as_uuid else str
    return column_type.python_type


def records_satisfy_table_constraints(records: List[RecordType],
                                      *,
                                      table: Table) -> bool:
    def all_unique(iterable: Iterable[Hashable]) -> bool:
        seen = set()
        for element in iterable:
            if element in seen:
                return False
            seen.add(element)
        return True

    return all(all_unique(record[index] for record in records)
               for index, column in enumerate(table.columns)
               if is_column_unique(column))
