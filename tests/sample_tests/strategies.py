from functools import partial
from typing import (Any,
                    Dict,
                    Tuple)

from hypothesis import strategies
from sqlalchemy.dialects import (mysql,
                                 postgresql,
                                 sqlite)
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.schema import (Column,
                               Table)

from hypothesis_sqlalchemy import scheme
from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.sample import column_type_scalars
from tests.utils import (MAX_MIN_SIZE,
                         MAX_SIZE)

data = strategies.data()
dialects = (strategies.one_of([strategies.builds(dialect)
                               for dialect in [DefaultDialect,
                                               mysql.dialect,
                                               postgresql.dialect,
                                               sqlite.dialect]]))
# for simplest table with single-value enum column
min_table_records_lists_sizes = strategies.integers(0, 1)
max_table_records_lists_sizes = (
        strategies.none() | strategies.integers(MAX_MIN_SIZE + 1, MAX_SIZE)
)
tables = dialects.flatmap(scheme.tables)


def fix_columns_values(table: Table
                       ) -> Strategy[Tuple[Table, Dict[str, Strategy[Any]]]]:
    def to_item(column: Column) -> Tuple[str, Strategy[Any]]:
        return column.name, column_type_scalars(column.type)

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
