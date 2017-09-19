from typing import (Any,
                    Callable)

from hypothesis import strategies
from sqlalchemy.schema import Table

from . import columns
from .types import Strategy
from .utils import identifiers


def tables_factory(
        *,
        tables_names: Strategy = identifiers,
        metadatas: Strategy,
        columns_lists: Strategy = columns.non_all_unique_lists_factory(),
        extend_existing: Strategy = strategies.just(True)) -> Strategy:
    @strategies.composite
    def factory(draw: Callable[[Strategy], Any]) -> Table:
        table_name = draw(tables_names)
        metadata = draw(metadatas)
        columns_list = draw(columns_lists)
        return Table(table_name,
                     metadata,
                     *columns_list,
                     extend_existing=draw(extend_existing))

    return factory()
