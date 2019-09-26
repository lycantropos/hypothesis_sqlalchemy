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
            extending_existing: Strategy[bool] = strategies.booleans()
            ) -> Strategy[Table]:
    if names is None:
        names = to_sql_identifiers(dialect)
    if columns is None:
        columns = columnar.factory(dialect,
                                   names=names)
    columns_lists = columnar.lists_factory(columns,
                                           min_size=min_size,
                                           max_size=max_size)

    def table_factory(draw: Callable[[Strategy], Any]) -> Table:
        extend_existing = draw(extending_existing)
        if extend_existing:
            table_names = names
        else:
            table_names = (names
                           .filter(lambda identifier:
                                   identifier not in metadata.tables))
        table_name = draw(table_names)
        columns_list = draw(columns_lists)
        if extend_existing and table_name in metadata.tables:
            # preserving constraints, especially primary key one
            existing_table = metadata.tables[table_name]
            columns_list = [existing_table.c.get(column.name, column)
                            for column in columns_list]
        result = Table(table_name,
                       metadata,
                       *columns_list,
                       extend_existing=extend_existing)
        constraints = draw(constrained.lists_factory(columns_list,
                                                     primary_key_min_size=1))
        for constraint in constraints:
            result.append_constraint(constraint)
        return result

    return strategies.composite(table_factory)()
