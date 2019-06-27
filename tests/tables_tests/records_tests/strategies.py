from functools import partial
from operator import attrgetter
from typing import (Any,
                    Dict,
                    Tuple)

from hypothesis import strategies
from sqlalchemy.schema import (Column,
                               Table)

from hypothesis_sqlalchemy import (columns,
                                   tables)
from hypothesis_sqlalchemy.columns import values
from hypothesis_sqlalchemy.hints import Strategy
from tests.strategies import (data,
                              max_sizes,
                              metadatas,
                              min_sizes)

data = data
min_sizes = min_sizes
max_sizes = max_sizes
non_unique_columns = columns.non_primary_keys_factory(
        are_unique=strategies.just(False))
tables_without_unique_columns = tables.factory(
        metadatas=metadatas,
        columns_lists=strategies.lists(non_unique_columns,
                                       unique_by=attrgetter('name')))
tables_with_unique_columns = tables.factory(metadatas=metadatas)
tables = tables_without_unique_columns | tables_with_unique_columns


def fix_columns_values(table: Table
                       ) -> Strategy[Tuple[Table, Dict[str, Strategy[Any]]]]:
    def to_item(column: Column) -> Tuple[str, Strategy[Any]]:
        return column.name, values.factory(column)

    fixed_columns_values = (strategies.sets(strategies
                                            .sampled_from(list(table.columns)))
                            .map(partial(map, to_item))
                            .map(dict))
    return strategies.tuples(strategies.just(table), fixed_columns_values)


tables_with_fixed_columns_values = tables.flatmap(fix_columns_values)
