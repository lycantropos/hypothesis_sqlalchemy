import uuid
from typing import Any

from hypothesis import (Phase,
                        core,
                        settings)
from hypothesis.errors import (NoSuchExample,
                               Unsatisfiable)
from hypothesis.searchstrategy import SearchStrategy
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID

from hypothesis_sqlalchemy.types import RecordType


def example(strategy: SearchStrategy) -> Any:
    first_object_list = []

    def condition(object_: Any) -> bool:
        if first_object_list:
            return True
        else:
            first_object_list.append(object_)
            return False

    try:
        return core.find(strategy,
                         condition,
                         settings=settings(database=None,
                                           phases=tuple(set(Phase)
                                                        - {Phase.shrink})))
    except (NoSuchExample, Unsatisfiable) as search_error:
        try:
            result, = first_object_list
        except ValueError as unpacking_error:
            raise unpacking_error from search_error
        else:
            return result


def table_record_is_valid(table_record: RecordType,
                          *,
                          table: Table) -> bool:
    return all(coordinate is None
               and column.nullable
               or isinstance(column.type, UUID)
               and isinstance(coordinate, uuid.UUID)
               or isinstance(coordinate, column.type.python_type)
               for coordinate, column in zip(table_record, table.columns))
