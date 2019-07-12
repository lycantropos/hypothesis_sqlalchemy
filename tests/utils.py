from typing import List

from sqlalchemy import Table

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
               or isinstance(coordinate, column.type.python_type)
               for coordinate, column in zip(table_record, table.columns))

def records_satisfy_table_constraints(records: List[RecordType],
                                      *,
                                      table: Table) -> bool:
    unique_indices = [index
                      for index, column in enumerate(table.columns)
                      if is_column_unique(column)]
    # All returned values are unique for the columns marked as unique
    return all(len({record[index] for record in records}) == len(records)
               for index in unique_indices)
