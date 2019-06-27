from typing import (Any,
                    Callable,
                    List,
                    Optional)

from hypothesis import strategies
from sqlalchemy.schema import (Column,
                               MetaData,
                               Table)

from hypothesis_sqlalchemy import columnar
from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.utils import sql_identifiers


def factory(*,
            tables_names: Strategy[str] = sql_identifiers,
            metadatas: Strategy[MetaData],
            columns_factory: Callable[..., Strategy[List[Column]]] =
            columnar.non_all_unique_lists_factory,
            min_size: int = 0,
            max_size: Optional[int] = None,
            extend_existing: Strategy[bool] = strategies.just(True)
            ) -> Strategy:
    columns_lists = columns_factory(min_size=min_size,
                                    max_size=max_size)

    def table_factory(draw: Callable[[Strategy], Any]) -> Table:
        table_name = draw(tables_names)
        metadata = draw(metadatas)
        columns_list = draw(columns_lists)
        return Table(table_name,
                     metadata,
                     *columns_list,
                     extend_existing=draw(extend_existing))

    return strategies.composite(table_factory)()
