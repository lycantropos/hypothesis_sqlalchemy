from typing import (Any,
                    Callable,
                    Optional)

from hypothesis import strategies
from sqlalchemy.engine import Dialect
from sqlalchemy.schema import (Column,
                               MetaData,
                               Table)

from hypothesis_sqlalchemy import (columnar,
                                   constrained,
                                   dialectic)
from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.utils import to_sql_identifiers


def factory(*,
            dialect: Dialect = dialectic.default,
            metadata: MetaData,
            names: Optional[Strategy[str]] = None,
            columns: Strategy[Column] = None,
            min_size: int = 0,
            max_size: Optional[int] = None,
            extend_existing: Strategy[bool] = strategies.booleans()
            ) -> Strategy[Table]:
    names = to_sql_identifiers(dialect) if names is None else names
    columns = (columnar.factory(dialect)
               if columns is None else columns)
    columns_lists = columnar.lists_factory(columns,
                                           min_size=min_size,
                                           max_size=max_size)

    def table_factory(draw: Callable[[Strategy], Any]) -> Table:
        extends_existing = draw(extend_existing)
        table_names = names
        if not extends_existing:
            table_names = (table_names
                           .filter(lambda identifier:
                                   identifier not in metadata.tables))
        table_name = draw(table_names)
        columns_list = draw(columns_lists)
        if extends_existing and table_name in metadata.tables:
            # preserving constraints, especially primary key one
            existing_table = metadata.tables[table_name]
            columns_list = [existing_table.c.get(column.name, column)
                            for column in columns_list]
        result = Table(table_name,
                       metadata,
                       *columns_list,
                       extend_existing=extends_existing)
        constraints = draw(constrained.lists_factory(columns_list,
                                                     primary_key_min_size=1))
        for constraint in constraints:
            result.append_constraint(constraint)
        return result

    return strategies.composite(table_factory)()
