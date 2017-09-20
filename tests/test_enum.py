import datetime
from enum import (EnumMeta,
                  Enum,
                  IntEnum)

import pytest
from hypothesis import strategies
from hypothesis.searchstrategy import SearchStrategy
from sqlalchemy.sql.sqltypes import Enum as EnumType

from hypothesis_sqlalchemy.enums import (factory,
                                         types_factory)
from tests.utils import example


def test_enums_factory() -> None:
    none_enums = factory(values=strategies.just(None))
    none_enum = example(none_enums)
    int_enums = factory(bases=strategies.tuples(strategies.just(IntEnum)))
    int_enum = example(int_enums)
    datetimes_enums = factory(bases=strategies.tuples(strategies.just(Enum)),
                              values=strategies.datetimes(),
                              datetime=datetime)
    datetimes_enum = example(datetimes_enums)
    invalid_keys_enums = factory(keys=strategies.none())
    invalid_values_enums = factory(
            bases=strategies.tuples(strategies.just(IntEnum)),
            values=strategies.none())

    assert isinstance(none_enums, SearchStrategy)
    assert isinstance(int_enums, SearchStrategy)
    assert isinstance(datetimes_enums, SearchStrategy)
    assert isinstance(none_enum, EnumMeta)
    assert isinstance(int_enum, EnumMeta)
    assert isinstance(datetimes_enum, EnumMeta)
    assert issubclass(none_enum, Enum)
    assert issubclass(int_enum, IntEnum)
    assert issubclass(datetimes_enum, Enum)
    assert all(member.value is None
               for member in none_enum)
    assert all(isinstance(member, int)
               for member in int_enum)
    assert all(isinstance(member.value, datetime.datetime)
               for member in datetimes_enum)

    with pytest.raises(ValueError):
        example(invalid_keys_enums)

    with pytest.raises(TypeError):
        example(invalid_values_enums)


def test_enum_types_factory() -> None:
    enums = types_factory()
    enum = example(enums)

    assert isinstance(enums, SearchStrategy)
    assert isinstance(enum, EnumType)
