from datetime import (date,
                      datetime,
                      time,
                      timedelta)
from decimal import Decimal
from enum import Enum
from functools import (partial,
                       singledispatch)
from typing import (Iterable,
                    Optional,
                    Type,
                    Union)
from uuid import UUID

from hypothesis import strategies
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import Dialect
from sqlalchemy.sql.sqltypes import (BigInteger,
                                     Boolean,
                                     Date,
                                     DateTime,
                                     Enum as EnumType,
                                     Float,
                                     Integer,
                                     Interval,
                                     LargeBinary,
                                     Numeric,
                                     SmallInteger,
                                     String,
                                     Text,
                                     Time,
                                     exc)
from sqlalchemy.sql.type_api import (TypeEngine,
                                     to_instance)

from . import enum
from .hints import (Scalar,
                    Strategy)
from .utils import to_sql_identifiers

TypeOrInstance = Union[TypeEngine, Type[TypeEngine]]
EXTRA = [Numeric, Float, Boolean, Date, DateTime, Interval, Time]


def instances(dialect: Dialect,
              *,
              primary_key_types: Optional[Strategy[TypeEngine]] = None,
              string_types: Optional[Strategy[TypeEngine]] = None,
              binary_string_types: Optional[Strategy[TypeEngine]] = None,
              enum_types: Optional[Strategy[TypeEngine]] = None
              ) -> Strategy[TypeEngine]:
    if primary_key_types is None:
        primary_key_types = primary_keys(dialect)
    if string_types is None:
        string_types = (strings(dialect)
                        if _is_type_supported(Text,
                                              dialect=dialect)
                        else strategies.nothing())
    if binary_string_types is None:
        binary_string_types = (binary_strings(dialect)
                               if _is_type_supported(LargeBinary,
                                                     dialect=dialect)
                               else strategies.nothing())
    if enum_types is None:
        enum_types = (enums(dialect)
                      if _is_type_supported(EnumType(name='_'),
                                            dialect=dialect)
                      else strategies.nothing())
    extra_types = list(_filter_unsupported_types(EXTRA,
                                                 dialect=dialect))
    return strategies.one_of(primary_key_types,
                             (strategies.sampled_from(extra_types)
                              .map(to_instance)),
                             string_types,
                             binary_string_types,
                             enum_types)


def binary_strings(dialect: Dialect,
                   *,
                   lengths: Strategy[int] = strategies.none()
                   ) -> Strategy[TypeEngine]:
    return strategies.builds(LargeBinary,
                             length=lengths)


def enums(dialect: Dialect,
          *,
          names: Optional[Strategy[str]] = None,
          values: Optional[Strategy[str]] = None,
          min_size: int = 1,
          max_size: Optional[int] = None) -> Strategy[TypeEngine]:
    if names is None:
        names = to_sql_identifiers(dialect)
    if values is None:
        values = to_sql_identifiers(dialect)
    enums_keys = values.filter(enum.is_valid_key)
    args = (strategies.tuples(enum.types(keys=enums_keys,
                                         min_size=min_size,
                                         max_size=max_size))
            | strategies.lists(values,
                               min_size=min_size,
                               max_size=max_size))
    return (strategies.tuples(names, args)
            .map(lambda name_with_args: EnumType(*name_with_args[1],
                                                 name=name_with_args[0])))


def primary_keys(dialect: Dialect) -> Strategy[TypeEngine]:
    types = list(_filter_unsupported_types([SmallInteger, Integer, BigInteger,
                                            postgresql.UUID],
                                           dialect=dialect))
    return strategies.sampled_from(types).map(to_instance)


def strings(dialect: Dialect,
            *,
            lengths: Strategy[int] = strategies.none()
            ) -> Strategy[TypeEngine]:
    return strategies.builds(Text,
                             length=lengths)


@singledispatch
def scalars(type_: TypeEngine) -> Strategy[Scalar]:
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


@scalars.register(String)
def _(type_: String,
      *,
      alphabet: Strategy = _ascii_not_null_characters) -> Strategy[str]:
    return strategies.text(alphabet=alphabet,
                           max_size=type_.length)


@scalars.register(LargeBinary)
def _(type_: LargeBinary) -> Strategy[bytes]:
    return strategies.binary(max_size=type_.length)


@scalars.register(EnumType)
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


@scalars.register(postgresql.UUID)
def _(type_: postgresql.UUID,
      *,
      version: Optional[int] = None) -> Strategy[Union[str, UUID]]:
    result = strategies.uuids(version=version)
    if not type_.as_uuid:
        result = result.map(str)
    return result


def _filter_unsupported_types(types_or_instances: Iterable[TypeOrInstance],
                              *,
                              dialect: Dialect) -> Iterable[TypeOrInstance]:
    return filter(partial(_is_type_supported,
                          dialect=dialect),
                  types_or_instances)


def _is_type_supported(type_or_instance: Type[TypeOrInstance],
                       *,
                       dialect: Dialect) -> bool:
    instance = to_instance(type_or_instance)
    try:
        instance.compile(dialect)
    except exc.UnsupportedCompilationError:
        return False
    else:
        return True
