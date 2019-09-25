from typing import Optional

from hypothesis import given
from sqlalchemy.engine import Dialect
from sqlalchemy.sql.sqltypes import Enum as EnumType

from hypothesis_sqlalchemy.columnar.types import enums_factory
from hypothesis_sqlalchemy.hints import Strategy
from tests import strategies
from tests.utils import DataObject


@given(strategies.dialects, strategies.min_sizes, strategies.max_sizes)
def test_basic(dialect: Dialect,
               min_size: int,
               max_size: Optional[int]) -> None:
    result = enums_factory(dialect,
                           min_size=min_size,
                           max_size=max_size)

    assert isinstance(result, Strategy)


@given(strategies.data, strategies.dialects,
       strategies.min_sizes, strategies.max_sizes)
def test_enum_types_factory(data: DataObject,
                            dialect: Dialect,
                            min_size: int,
                            max_size: Optional[int]) -> None:
    strategy = enums_factory(dialect,
                             min_size=min_size,
                             max_size=max_size)

    result = data.draw(strategy)

    assert isinstance(result, EnumType)
    assert min_size <= len(result.enums)
    assert max_size is None or len(result.enums) <= max_size
