from collections import OrderedDict
from datetime import (date,
                      datetime)
from decimal import Decimal
from functools import (partial,
                       singledispatch)
from typing import (Any,
                    Iterable,
                    List,
                    Tuple)

from hypothesis import strategies
from hypothesis.searchstrategy.collections import TupleStrategy
from hypothesis.strategies import none
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import (Enum,
                                     String)
from sqlalchemy.sql.type_api import TypeEngine

from .types import Strategy
from .utils import (MAX_RECORDS_COUNT,
                    MIN_RECORDS_COUNT,
                    is_column_unique)

# we're using integers as primary key values
# which are usually positive
MIN_POSITIVE_INTEGER_VALUE = 1
MAX_SMALLINT_VALUE = 32767

MIN_DATE_TIME = datetime.utcfromtimestamp(0)


def factory(columns: Iterable[Column],
            **fixed_columns_values: Strategy
            ) -> TupleStrategy:
    columns_values_strategies = OrderedDict(
            (column.name,
             strategies.one_of(column_values_factory(column),
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
    values_tuples = factory(columns,
                            **fixed_columns_values)
    unique_indices = [index
                      for index, column in enumerate(columns)
                      if is_column_unique(column)]

    def to_unique_fields(row: Tuple[Any, ...]) -> Tuple[Any, ...]:
        return tuple(row[index] for index in unique_indices)

    return strategies.lists(values_tuples,
                            min_size=min_size,
                            max_size=max_size,
                            unique_by=to_unique_fields)


booleans_factory = strategies.booleans


def integers_factory(min_value: int = MIN_POSITIVE_INTEGER_VALUE,
                     max_value: int = MAX_SMALLINT_VALUE) -> Strategy:
    return strategies.integers(min_value=min_value,
                               max_value=max_value)


def floats_factory(*,
                   min_value: float = None,
                   max_value: float = None,
                   allow_nan: bool = False,
                   allow_infinity: bool = False) -> Strategy:
    return strategies.floats(min_value=min_value,
                             max_value=max_value,
                             allow_nan=allow_nan,
                             allow_infinity=allow_infinity)


def decimals_factory(*,
                     min_value: float = None,
                     max_value: float = None,
                     allow_nan: bool = False,
                     allow_infinity: bool = False,
                     places: int = None) -> Strategy:
    return strategies.decimals(min_value=min_value,
                               max_value=max_value,
                               allow_nan=allow_nan,
                               allow_infinity=allow_infinity,
                               places=places)


def date_times_factory(*,
                       min_value: datetime = MIN_DATE_TIME,
                       max_value: datetime = datetime.max,
                       timezones: Strategy = none()) -> Strategy:
    date_times = strategies.datetimes(min_value=min_value,
                                      max_value=max_value,
                                      timezones=timezones)
    return date_times.map(partial(datetime.replace,
                                  microsecond=0))


def dates_factory(min_value: date = MIN_DATE_TIME.date(),
                  max_value: date = date.max) -> Strategy:
    return strategies.dates(min_value=min_value,
                            max_value=max_value)


values_by_python_types = {
    bool: booleans_factory(),
    int: integers_factory(),
    float: floats_factory(),
    Decimal: decimals_factory(),
    datetime: date_times_factory(),
    date: dates_factory(),
}


@singledispatch
def from_column_type(column_type: TypeEngine) -> Strategy:
    return values_by_python_types[column_type.python_type]


ascii_not_null_characters = strategies.characters(min_codepoint=1,
                                                  max_codepoint=127)


@from_column_type.register(String)
def string_type_values_factory(string_type: String,
                               *,
                               alphabet: Strategy = ascii_not_null_characters
                               ) -> Strategy:
    return strategies.text(alphabet=alphabet,
                           max_size=string_type.length)


@from_column_type.register(Enum)
def enum_type_values_factory(enum_type: Enum) -> Strategy:
    enum_class = enum_type.enum_class
    # The source of enumerated values may be a list of string values
    if enum_class is None:
        return strategies.one_of(*map(strategies.just,
                                      enum_type.enums))
    # ... or a PEP-435-compliant enumerated class.
    # More info at
    # http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Enum
    return strategies.one_of(*map(strategies.just,
                                  enum_class))


@from_column_type.register(UUID)
def uuid_type_values_factory(_: UUID) -> Strategy:
    return strategies.uuids()


factories_by_sql_types = {
    String: string_type_values_factory,
    Enum: enum_type_values_factory,
    UUID: uuid_type_values_factory,
}


def column_values_factory(column: Column) -> Strategy:
    return from_column_type(column.type)
