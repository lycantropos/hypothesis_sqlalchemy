"""Strategies for generating ``SQLAlchemy`` objects."""

from .core import (column as _column,
                   column_type as _column_type,
                   table as _table)

column_types = _column_type.instances
columns = _column.instances
tables = _table.instances
