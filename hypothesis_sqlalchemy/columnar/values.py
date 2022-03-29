from datetime import (date,
                      datetime,
                      time,
                      timedelta)
from decimal import Decimal
from enum import Enum
from functools import singledispatch
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


def factory(column: Column) -> Strategy:
    return from_type(column.type)


@singledispatch
def from_type(type_: TypeEngine) -> Strategy[Any]:
    return _values_by_python_types[type_.python_type]


# we're using integers as primary key values
# which are usually positive
_MIN_POSITIVE_INTEGER_VALUE = 1
_MAX_SMALLINT_VALUE = 32767
_ascii_not_null_characters = strategies.characters(min_codepoint=1,
                                                   max_codepoint=127)
_values_by_python_types = {
    bool: strategies.booleans(),
    int: strategies.integers(min_value=_MIN_POSITIVE_INTEGER_VALUE,
                             max_value=_MAX_SMALLINT_VALUE),
    float: strategies.floats(allow_nan=False,
                             allow_infinity=False),
    Decimal: strategies.decimals(allow_nan=False,
                                 allow_infinity=False),
    datetime: strategies.datetimes(),
    date: strategies.dates(),
    time: strategies.times(),
    timedelta: strategies.timedeltas(),
}


@from_type.register(String)
def _(type_: String,
      *,
      alphabet: Strategy = _ascii_not_null_characters) -> Strategy[str]:
    return strategies.text(alphabet=alphabet,
                           max_size=type_.length)


@from_type.register(LargeBinary)
def _(type_: LargeBinary) -> Strategy[bytes]:
    return strategies.binary(max_size=type_.length)


@from_type.register(EnumType)
def _(type_: EnumType) -> Strategy[Union[str, Enum]]:
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
def _(type_: postgresql.UUID,
      *,
      version: Optional[int] = None) -> Strategy[Union[str, UUID]]:
    result = strategies.uuids(version=version)
    if not type_.as_uuid:
        result = result.map(str)
    return result
