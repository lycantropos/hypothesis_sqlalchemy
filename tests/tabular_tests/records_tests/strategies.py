from functools import partial
from operator import attrgetter
from typing import (Any,
                    Dict,
                    List,
                    Optional,
                    Tuple)

from hypothesis import strategies
from sqlalchemy.engine import Dialect
from sqlalchemy.schema import (Column,
                               Table)

from hypothesis_sqlalchemy import (columnar,
                                   tabular)
from hypothesis_sqlalchemy.columnar import values
from hypothesis_sqlalchemy.hints import Strategy
from tests.strategies import (data,
                              dialects,
                              max_sizes,
                              metadatas,
                              min_sizes)

data = data
min_sizes = min_sizes
max_sizes = max_sizes


def to_non_unique_columns(dialect: Dialect,
                          *,
                          min_size: int,
                          max_size: Optional[int]) -> Strategy[List[Column]]:
    non_unique_columns = columnar.non_primary_keys_factory(
            dialect,
            are_unique=strategies.just(False))
    return strategies.lists(non_unique_columns,
                            min_size=min_size,
                            max_size=max_size,
                            unique_by=attrgetter('name'))


tables_without_unique_columns = strategies.tuples(dialects, metadatas).flatmap(
        lambda dialect_with_metadata: tabular.factory(
                dialect=dialect_with_metadata[0],
                metadata=dialect_with_metadata[1],
                columns_factory=to_non_unique_columns))
tables_with_unique_columns = strategies.tuples(dialects, metadatas).flatmap(
        lambda dialect_with_metadata: tabular.factory(
                dialect=dialect_with_metadata[0],
                metadata=dialect_with_metadata[1]))
tables = tables_without_unique_columns | tables_with_unique_columns


def fix_columns_values(table: Table
                       ) -> Strategy[Tuple[Table, Dict[str, Strategy[Any]]]]:
    def to_item(column: Column) -> Tuple[str, Strategy[Any]]:
        return column.name, values.factory(column)

    if table.columns:
        fixed_columns_values = (strategies.sets(
                strategies.sampled_from(list(table.columns)))
                                .map(partial(map, to_item))
                                .map(dict))
    else:
        fixed_columns_values = strategies.builds(dict)
    return strategies.tuples(strategies.just(table), fixed_columns_values)


tables_with_fixed_columns_values = tables.flatmap(fix_columns_values)
