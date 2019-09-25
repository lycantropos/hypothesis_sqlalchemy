from functools import partial
from typing import (Iterable,
                    Optional,
                    Type,
                    Union)

from hypothesis import strategies
from sqlalchemy import exc
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import Dialect
from sqlalchemy.sql.sqltypes import (BigInteger,
                                     Boolean,
                                     Date,
                                     DateTime,
                                     Enum,
                                     Float,
                                     Integer,
                                     Interval,
                                     LargeBinary,
                                     Numeric,
                                     SmallInteger,
                                     String,
                                     Time)
from sqlalchemy.sql.type_api import (TypeEngine,
                                     to_instance)

from hypothesis_sqlalchemy import enumerable
from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.utils import to_sql_identifiers

TypeOrInstance = Union[TypeEngine, Type[TypeEngine]]


def strings_factory(dialect: Dialect,
                    *,
                    lengths: Strategy[int] = strategies.none()
                    ) -> Strategy[TypeEngine]:
    return strategies.builds(String,
                             length=lengths)


def binary_strings_factory(dialect: Dialect,
                           *,
                           lengths: Strategy[int] = strategies.none()
                           ) -> Strategy[TypeEngine]:
    return strategies.builds(LargeBinary,
                             length=lengths)


def filter_unsupported_types(types_or_instances: Iterable[TypeOrInstance],
                             *,
                             dialect: Dialect) -> Iterable[TypeOrInstance]:
    return filter(partial(is_type_supported,
                          dialect=dialect),
                  types_or_instances)


def is_type_supported(type_or_instance: Type[TypeOrInstance],
                      *,
                      dialect: Dialect) -> bool:
    instance = to_instance(type_or_instance)
    try:
        instance.compile(dialect)
    except exc.UnsupportedCompilationError:
        return False
    else:
        return True


def primary_keys_factory(dialect: Dialect) -> Strategy[TypeEngine]:
    types = list(filter_unsupported_types([SmallInteger, Integer, BigInteger,
                                           postgresql.UUID],
                                          dialect=dialect))
    return strategies.sampled_from(types).map(to_instance)


def enums_factory(dialect: Dialect,
                  *,
                  values: Optional[Strategy[str]] = None,
                  min_size: int = 1,
                  max_size: Optional[int] = None) -> Strategy[TypeEngine]:
    if values is None:
        values = to_sql_identifiers(dialect)
    enums_keys = values.filter(enumerable.is_valid_key)
    return ((strategies.tuples(enumerable.factory(keys=enums_keys,
                                                  min_size=min_size,
                                                  max_size=max_size))
             | strategies.lists(values,
                                min_size=min_size,
                                max_size=max_size))
            .map(lambda type_values: Enum(*type_values)))


EXTRA_COLUMNS_TYPES = [Numeric, Float, Boolean, Date, DateTime, Interval, Time]


def factory(dialect: Dialect,
            *,
            primary_keys_types: Optional[Strategy[TypeEngine]] = None,
            string_types: Optional[Strategy[TypeEngine]] = None,
            binary_string_types: Optional[Strategy[TypeEngine]] = None,
            enum_types: Optional[Strategy[TypeEngine]] = None
            ) -> Strategy[TypeEngine]:
    if primary_keys_types is None:
        primary_keys_types = primary_keys_factory(dialect)
    if string_types is None:
        string_types = strings_factory(dialect)
    if binary_string_types is None:
        binary_string_types = binary_strings_factory(dialect)
    if enum_types is None:
        enum_types = enums_factory(dialect)
    extra_types = list(filter_unsupported_types(EXTRA_COLUMNS_TYPES,
                                                dialect=dialect))
    return strategies.one_of(primary_keys_types,
                             strategies.sampled_from(extra_types),
                             string_types,
                             binary_string_types,
                             enum_types)
