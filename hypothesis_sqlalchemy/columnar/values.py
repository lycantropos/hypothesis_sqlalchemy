from datetime import (date,
                      datetime,
                      time,
                      timedelta)
from decimal import Decimal
from enum import Enum
from functools import (partial,
                       singledispatch)
from typing import (Any,
                    Optional,
                    Union)
from uuid import UUID

from hypothesis import strategies
from sqlalchemy import (Column,
                        Enum as EnumType,
                        LargeBinary,
                        String)
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.type_api import TypeEngine

from hypothesis_sqlalchemy.hints import Strategy

# we're using integers as primary key values
# which are usually positive
MIN_POSITIVE_INTEGER_VALUE = 1
MAX_SMALLINT_VALUE = 32767
MIN_DATE_TIME = datetime.utcfromtimestamp(0)


def factory(column: Column) -> Strategy:
    return from_type(column.type)


to_booleans = strategies.booleans
to_integers = strategies.integers
to_floats = strategies.floats
to_decimals = strategies.decimals


def to_date_times(*,
                  min_value: datetime = datetime.min,
                  max_value: datetime = datetime.max,
                  timezones: Strategy = strategies.none()) -> Strategy:
    date_times = strategies.datetimes(min_value=min_value,
                                      max_value=max_value,
                                      timezones=timezones)
    return date_times.map(partial(datetime.replace,
                                  microsecond=0))


to_dates = strategies.dates

values_by_python_types = {
    bool: to_booleans(),
    int: to_integers(min_value=MIN_POSITIVE_INTEGER_VALUE,
                     max_value=MAX_SMALLINT_VALUE),
    float: to_floats(allow_nan=False,
                     allow_infinity=False),
    Decimal: to_decimals(allow_nan=False,
                         allow_infinity=False),
    datetime: to_date_times(min_value=MIN_DATE_TIME),
    date: to_dates(min_value=MIN_DATE_TIME.date()),
    time: strategies.times(),
    timedelta: strategies.timedeltas(),
}


@singledispatch
def from_type(type_: TypeEngine) -> Strategy[Any]:
    return values_by_python_types[type_.python_type]


ascii_not_null_characters = strategies.characters(min_codepoint=1,
                                                  max_codepoint=127)


@from_type.register(String)
def string_type_values_factory(type_: String,
                               *,
                               alphabet: Strategy = ascii_not_null_characters
                               ) -> Strategy[str]:
    return strategies.text(alphabet=alphabet,
                           max_size=type_.length)


@from_type.register(LargeBinary)
def binary_string_type_values_factory(type_: LargeBinary) -> Strategy[bytes]:
    return strategies.binary(max_size=type_.length)


@from_type.register(EnumType)
def enum_type_values_factory(type_: EnumType) -> Strategy[Union[str, Enum]]:
    enum_class = type_.enum_class
    if enum_class is None:
        # The source of enumerated values may be a list of string values
        values = type_.enums
    else:
        # ... or a PEP-435-compliant enumerated class.
        # More info at
        # http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Enum
        values = list(enum_class)
    return strategies.sampled_from(values)


@from_type.register(postgresql.UUID)
def uuid_type_values_factory(type_: postgresql.UUID,
                             *,
                             version: Optional[int] = None
                             ) -> Strategy[Union[str, UUID]]:
    result = strategies.uuids(version)
    if not type_.as_uuid:
        result = result.map(str)
    return result
