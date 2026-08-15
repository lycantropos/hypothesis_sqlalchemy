from collections.abc import Iterable, Mapping, Sequence
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum
from functools import partial, singledispatch
from typing import Any, Final, Literal, TypeAlias
from uuid import UUID

from hypothesis import strategies as st
from sqlalchemy import exc
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import Dialect
from sqlalchemy.sql.sqltypes import (
    BigInteger,
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
)
from sqlalchemy.sql.type_api import TypeEngine, to_instance

from . import enum
from .hints import Scalar, Strategy
from .utils import to_sql_identifiers

TypeOrInstance: TypeAlias = TypeEngine[Any] | type[TypeEngine[Any]]
EXTRA: Final[Sequence[TypeOrInstance]] = [
    Numeric,
    Float,
    Boolean,
    Date,
    DateTime,
    Interval,
    Time,
]


def instances(
    dialect: Dialect,
    *,
    primary_key_types: Strategy[TypeEngine[Any]] | None = None,
    string_types: Strategy[TypeEngine[Any]] | None = None,
    binary_string_types: Strategy[TypeEngine[Any]] | None = None,
    enum_types: Strategy[TypeEngine[Any]] | None = None,
) -> Strategy[TypeEngine[Any]]:
    if primary_key_types is None:
        primary_key_types = primary_keys(dialect)
    if string_types is None:
        string_types = (
            strings(dialect)
            if _is_type_supported(Text, dialect=dialect)
            else st.nothing()
        )
    if binary_string_types is None:
        binary_string_types = (
            binary_strings(dialect)
            if _is_type_supported(LargeBinary, dialect=dialect)
            else st.nothing()
        )
    if enum_types is None:
        enum_types = (
            enums(dialect)
            if _is_type_supported(EnumType(name='_'), dialect=dialect)
            else st.nothing()
        )
    extra_types = list(_filter_unsupported_types(EXTRA, dialect=dialect))
    return (
        primary_key_types
        | st.sampled_from(extra_types).map(to_instance)
        | string_types
        | binary_string_types
        | enum_types
    )


def binary_strings(
    dialect: Dialect,  # ruff: ignore[unused-function-argument]
    *,
    lengths: Strategy[int | None] = st.none(),  # ruff: ignore[function-call-in-default-argument]
) -> Strategy[TypeEngine[bytes]]:
    return st.builds(LargeBinary, length=lengths)


def enums(
    dialect: Dialect,
    *,
    names: Strategy[str] | None = None,
    values: Strategy[str] | None = None,
    min_size: int = 1,
    max_size: int | None = None,
) -> Strategy[TypeEngine[Any]]:
    if names is None:
        names = to_sql_identifiers(dialect)
    if values is None:
        values = to_sql_identifiers(dialect)
    enums_keys = values.filter(enum.is_valid_key)
    args = st.tuples(
        enum.types(keys=enums_keys, min_size=min_size, max_size=max_size)
    ) | st.lists(values, min_size=min_size, max_size=max_size)
    return st.builds(_build_enum_type, names, args)


def _build_enum_type(
    name: str, args: tuple[type[Enum]] | Sequence[str]
) -> EnumType:
    return EnumType(  # pyright: ignore[reportCallIssue]
        *args,  # pyright: ignore[reportArgumentType]
        name=name,
    )


def primary_keys(dialect: Dialect) -> Strategy[TypeEngine[Any]]:
    types = list(
        _filter_unsupported_types(
            [
                SmallInteger,
                Integer,
                BigInteger,
                postgresql.UUID(as_uuid=False),
                postgresql.UUID(as_uuid=True),
            ],
            dialect=dialect,
        )
    )
    return st.sampled_from(types).map(to_instance)


def strings(
    dialect: Dialect,  # ruff: ignore[unused-function-argument]
    *,
    lengths: Strategy[int | None] = st.none(),  # ruff: ignore[function-call-in-default-argument]
) -> Strategy[TypeEngine[str]]:
    return st.builds(Text, length=lengths)


@singledispatch
def scalars(type_: TypeEngine[Any]) -> Strategy[Scalar]:
    return _values_by_python_types[type_.python_type]


# we're using integers as primary key values
# which are usually positive
_MIN_POSITIVE_INTEGER_VALUE = 1
_MAX_SMALLINT_VALUE = 32767
_ascii_not_null_characters = st.characters(min_codepoint=1, max_codepoint=127)
_values_by_python_types: Mapping[type[Scalar], Strategy[Scalar]] = {
    bool: st.booleans(),
    int: st.integers(
        min_value=_MIN_POSITIVE_INTEGER_VALUE, max_value=_MAX_SMALLINT_VALUE
    ),
    float: st.floats(allow_nan=False, allow_infinity=False),
    Decimal: st.decimals(allow_nan=False, allow_infinity=False),
    datetime: st.datetimes(),
    date: st.dates(),
    time: st.times(),
    timedelta: st.timedeltas(),
}


@scalars.register(String)
def _(
    type_: String, *, alphabet: Strategy[str] = _ascii_not_null_characters
) -> Strategy[str]:
    return st.text(alphabet=alphabet, max_size=type_.length)


@scalars.register(LargeBinary)
def _(type_: LargeBinary) -> Strategy[bytes]:
    return st.binary(max_size=type_.length)


@scalars.register(EnumType)
def _(type_: EnumType) -> Strategy[str | Enum]:
    enum_class = type_.enum_class
    values = (
        # The source of enumerated values may be a list of string values
        type_.enums
        if enum_class is None
        # ... or a PEP-435-compliant enumerated class.
        # More info at
        # http://docs.sqlalchemy.org/en/latest/core/type_basics.html#sqlalchemy.types.Enum
        else list(enum_class)
    )
    return st.sampled_from(values)


@scalars.register(postgresql.UUID)
def _(
    type_: postgresql.UUID[Any],
    *,
    version: Literal[1, 2, 3, 4, 5] | None = None,
) -> Strategy[str | UUID]:
    result: Strategy[str | UUID] = st.uuids(version=version)
    if not type_.as_uuid:
        result = result.map(str)
    return result


def _filter_unsupported_types(
    types_or_instances: Iterable[TypeOrInstance], *, dialect: Dialect
) -> Iterable[TypeOrInstance]:
    return filter(
        partial(_is_type_supported, dialect=dialect), types_or_instances
    )


def _is_type_supported(
    type_or_instance: TypeOrInstance, *, dialect: Dialect
) -> bool:
    instance = to_instance(type_or_instance)
    try:
        instance.compile(dialect)
    except exc.UnsupportedCompilationError:
        return False
    else:
        return True
