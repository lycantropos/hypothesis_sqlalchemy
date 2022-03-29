from functools import partial
from typing import (Any,
                    Dict,
                    Tuple)

from hypothesis import strategies
from sqlalchemy.schema import (Column,
                               Table)

from hypothesis_sqlalchemy import tabular
from hypothesis_sqlalchemy.columnar import values
from hypothesis_sqlalchemy.hints import Strategy
from tests.strategies import (data,
                              dialects,
                              max_sizes,
                              metadatas)

data = data
# for simplest table with single-value enum column
min_sizes = strategies.integers(0, 1)
max_sizes = max_sizes
tables = dialects.flatmap(lambda dialect: tabular.factory(dialect=dialect,
                                                          metadatas=metadatas))


def fix_columns_values(table: Table
                       ) -> Strategy[Tuple[Table, Dict[str, Strategy[Any]]]]:
    def to_item(column: Column) -> Tuple[str, Strategy[Any]]:
        return column.name, values.factory(column)

    if table.columns:
        fixed_columns_values = (
            (strategies.sets(strategies.sampled_from(list(table.columns)))
             .map(partial(map, to_item))
             .map(dict))
        )
    else:
        fixed_columns_values = strategies.builds(dict)
    return strategies.tuples(strategies.just(table), fixed_columns_values)


tables_with_fixed_columns_values = tables.flatmap(fix_columns_values)
