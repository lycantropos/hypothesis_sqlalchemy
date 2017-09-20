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
    enums = factory()
    enum = example(enums)
    int_enums = factory(bases=strategies.tuples(strategies.just(IntEnum)))
    int_enum = example(int_enums)
    invalid_keys_enums = factory(keys=strategies.none())
    invalid_values_enums = factory(
        bases=strategies.tuples(strategies.just(IntEnum)),
        values=strategies.none())

    assert isinstance(enums, SearchStrategy)
    assert isinstance(int_enums, SearchStrategy)
    assert isinstance(enum, EnumMeta)
    assert isinstance(int_enum, EnumMeta)
    assert issubclass(enum, Enum)
    assert issubclass(int_enum, IntEnum)

    with pytest.raises(ValueError):
        example(invalid_keys_enums)

    with pytest.raises(TypeError):
        example(invalid_values_enums)


def test_enum_types_factory() -> None:
    enums = types_factory()
    enum = example(enums)

    assert isinstance(enums, SearchStrategy)
    assert isinstance(enum, EnumType)
