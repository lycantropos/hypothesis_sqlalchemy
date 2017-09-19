from typing import (Any,
                    Callable)

from hypothesis import strategies
from sqlalchemy.schema import Table

from hypothesis_sqlalchemy import columns
from hypothesis_sqlalchemy.types import Strategy
from hypothesis_sqlalchemy.utils import identifiers


def factory(
        *,
        tables_names: Strategy = identifiers,
        metadatas: Strategy,
        columns_lists: Strategy = columns.non_all_unique_lists_factory(),
        extend_existing: Strategy = strategies.just(True)) -> Strategy:
    def table_factory(draw: Callable[[Strategy], Any]) -> Table:
        table_name = draw(tables_names)
        metadata = draw(metadatas)
        columns_list = draw(columns_lists)
        return Table(table_name,
                     metadata,
                     *columns_list,
                     extend_existing=draw(extend_existing))

    return strategies.composite(table_factory)()
