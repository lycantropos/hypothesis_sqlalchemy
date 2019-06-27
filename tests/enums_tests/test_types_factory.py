from typing import Optional

from hypothesis import given
from sqlalchemy.sql.sqltypes import Enum as EnumType

from hypothesis_sqlalchemy.enums import types_factory
from hypothesis_sqlalchemy.hints import Strategy
from tests.utils import DataObject
from . import strategies


@given(strategies.min_sizes, strategies.max_sizes)
def test_basic(min_size: int, max_size: Optional[int]) -> None:
    result = types_factory(min_size=min_size,
                           max_size=max_size)

    assert isinstance(result, Strategy)


@given(strategies.data, strategies.min_sizes, strategies.max_sizes)
def test_enum_types_factory(data: DataObject,
                            min_size: int,
                            max_size: Optional[int]) -> None:
    strategy = types_factory(min_size=min_size,
                             max_size=max_size)

    result = data.draw(strategy)

    assert isinstance(result, EnumType)
    assert min_size <= len(result.enums)
    assert max_size is None or len(result.enums) <= max_size
