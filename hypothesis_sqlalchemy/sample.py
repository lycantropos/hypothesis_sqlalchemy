"""Strategies for generating data from ``SQLAlchemy`` objects."""

from .core import (column as _column,
                   column_type as _column_type,
                   columns_records as _columns_records,
                   table_records as _table_records)

column_type_scalars = _column_type.scalars
column_scalars = _column.scalars
columns_records = _columns_records.instances
columns_records_lists = _columns_records.lists
table_records = _table_records.instances
table_records_lists = _table_records.lists
