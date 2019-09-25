from typing import (Any,
                    Callable,
                    List,
                    Optional)

from hypothesis import strategies
from sqlalchemy.engine import Dialect
from sqlalchemy.schema import (Column,
                               MetaData,
                               Table)

from hypothesis_sqlalchemy import (columnar,
                                   dialectic)
from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.utils import to_sql_identifiers


def factory(*,
            dialect: Dialect = dialectic.default,
            metadata: MetaData,
            tables_names: Optional[Strategy[str]] = None,
            columns_factory: Callable[..., Strategy[List[Column]]] =
            columnar.non_all_unique_lists_factory,
            min_size: int = 0,
            max_size: Optional[int] = None,
            extend_existing: Strategy[bool] = strategies.just(True)
            ) -> Strategy:
    if tables_names is None:
        tables_names = to_sql_identifiers(dialect)
    columns_lists = columns_factory(dialect,
                                    min_size=min_size,
                                    max_size=max_size)

    def table_factory(draw: Callable[[Strategy], Any]) -> Table:
        table_name = draw(tables_names)
        columns_list = draw(columns_lists)
        return Table(table_name,
                     metadata,
                     *columns_list,
                     extend_existing=draw(extend_existing))

    return strategies.composite(table_factory)()
