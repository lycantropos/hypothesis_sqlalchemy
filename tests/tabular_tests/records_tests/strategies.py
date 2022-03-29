from functools import partial
from typing import (Any,
                    Dict,
                    Tuple)

from hypothesis import strategies
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
from tests.strategies.utils import MAX_MIN_SIZE

data = data
min_sizes = min_sizes
max_sizes = max_sizes

tables = dialects.flatmap(
        lambda dialect: tabular.factory(
                dialect=dialect,
                columns=columnar.factory(
                        dialect,
                        types=columnar.types.factory(
                                dialect,
                                enum_types=columnar.types.enums_factory(
                                        dialect,
                                        min_size=MAX_MIN_SIZE
                                )
                        )
                ),
                metadatas=metadatas
        )
)


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
