from operator import attrgetter
from typing import (Any,
                    Callable,
                    Optional)

from hypothesis import strategies
from sqlalchemy.engine import Dialect
from sqlalchemy.schema import (Column,
                               MetaData,
                               Table)

from . import (column,
               table_constraints)
from .hints import Strategy
from .utils import to_sql_identifiers


def instances(dialect: Dialect,
              *,
              metadatas: Strategy[MetaData] = strategies.builds(MetaData),
              names: Optional[Strategy[str]] = None,
              columns: Optional[Strategy[Column]] = None,
              min_size: int = 0,
              max_size: Optional[int] = None,
              extend_existing: Strategy[bool] = strategies.booleans()
              ) -> Strategy[Table]:
    tables_names = to_sql_identifiers(dialect) if names is None else names
    tables_columns = column.instances(dialect) if columns is None else columns
    tables_columns_lists = strategies.lists(tables_columns,
                                            min_size=min_size,
                                            max_size=max_size,
                                            unique_by=attrgetter('name'))

    def draw_table(draw: Callable[[Strategy], Any]) -> Table:
        metadata = draw(metadatas)
        extends_existing = draw(extend_existing)
        table_names = tables_names
        if not extends_existing:
            table_names = (table_names
                           .filter(lambda identifier:
                                   identifier not in metadata.tables))
        table_name = draw(table_names)
        columns_list = draw(tables_columns_lists)
        if extends_existing and table_name in metadata.tables:
            # preserving constraints, especially primary key one
            existing_table = metadata.tables[table_name]
            columns_list = [existing_table.c.get(column.name, column)
                            for column in columns_list]
        result = Table(table_name, metadata, *columns_list,
                       extend_existing=extends_existing)
        constraints = draw(table_constraints.lists(result,
                                                   primary_key_min_size=1))
        for constraint in constraints:
            result.append_constraint(constraint)
        return result

    return strategies.composite(draw_table)()
