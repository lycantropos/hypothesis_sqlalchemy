from datetime import (date,
                      datetime)
from decimal import Decimal
from itertools import (product,
                       islice)
from typing import (Iterable,
                    Iterator,
                    Dict,
                    Tuple,
                    List)

from collections import OrderedDict
from functools import partial
from hypothesis import strategies
from hypothesis.searchstrategy.collections import TupleStrategy
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import String

from .types import (Strategy,
                    ColumnValueType)
from .utils import (MIN_RECORDS_COUNT,
                    MAX_RECORDS_COUNT,
                    is_column_unique)

# we're using integers as primary key values
# which are usually positive
MIN_POSITIVE_INTEGER_VALUE = 1
MAX_SMALLINT_VALUE = 32767

MIN_DATE_TIME = datetime.utcfromtimestamp(0)
date_times = strategies.datetimes(min_value=MIN_DATE_TIME)
dates = strategies.dates(min_value=MIN_DATE_TIME.date())


def factory(columns: Iterable[Column],
            **fixed_columns_values: Strategy
            ) -> TupleStrategy:
    columns_values_strategies = OrderedDict(
            (column.name,
             strategies.one_of(
                     column_values_factory(column),
                     strategies.none())
             if column.nullable
             else column_values_factory(column))
            for column in columns)
    columns_values_strategies.update(fixed_columns_values)
    return strategies.tuples(*columns_values_strategies.values())


def lists_factory(columns: List[Column],
                  *,
                  min_size: int = MIN_RECORDS_COUNT,
                  max_size: int = MAX_RECORDS_COUNT,
                  **fixed_columns_values: Strategy
                  ) -> TupleStrategy:
    values_lists = columns_values_lists(columns,
                                        min_size=min_size,
                                        max_size=max_size,
                                        **fixed_columns_values)

    def to_records(values: Tuple[List[ColumnValueType], ...]
                   ) -> Iterator[Tuple[ColumnValueType]]:
        return list(islice(product(*values), 0, MAX_RECORDS_COUNT))

    tuples = strategies.tuples(*values_lists)
    return tuples.map(to_records)


def columns_values_lists(columns: Iterable[Column],
                         *,
                         max_size: int,
                         min_size: int,
                         **fixed_columns_values: Strategy
                         ) -> Iterator[Strategy]:
    for column in columns:
        column_name = column.name
        if column_name in fixed_columns_values:
            values = fixed_columns_values[column_name]
        else:
            values = column_values_factory(column)
        yield strategies.lists(values,
                               min_size=min_size,
                               max_size=max_size,
                               unique=is_column_unique(column))


strategies_by_python_types = {
    bool: strategies.booleans(),
    int: strategies.integers(min_value=MIN_POSITIVE_INTEGER_VALUE,
                             max_value=MAX_SMALLINT_VALUE),
    float: strategies.floats(allow_nan=False,
                             allow_infinity=False),
    Decimal: strategies.decimals(allow_nan=False,
                                 allow_infinity=False),
    datetime: date_times.map(partial(datetime.replace,
                                     microsecond=0)),
    date: dates,
}

ascii_not_null_characters = strategies.characters(min_codepoint=1,
                                                  max_codepoint=127)


def column_values_factory(column: Column) -> Strategy:
    column_type = column.type
    if isinstance(column_type, String):
        return strategies.text(alphabet=ascii_not_null_characters,
                               max_size=column_type.length)
    return strategies_by_python_types[column_type.python_type]
