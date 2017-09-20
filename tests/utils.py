import uuid
from typing import Any

from hypothesis import (Verbosity,
                        find,
                        settings)
from hypothesis.searchstrategy import SearchStrategy
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID

from hypothesis_sqlalchemy.types import RecordType


def example(strategy: SearchStrategy) -> Any:
    return find(specifier=strategy,
                condition=lambda x: True,
                settings=settings(max_shrinks=0,
                                  max_iterations=10000,
                                  verbosity=Verbosity.quiet))


def table_record_is_valid(table_record: RecordType,
                          *,
                          table: Table) -> bool:
    return all(coordinate is None and column.nullable or
               isinstance(column.type, UUID) and
               isinstance(coordinate, uuid.UUID) or
               isinstance(coordinate, column.type.python_type)
               for coordinate, column in zip(table_record, table.columns))
