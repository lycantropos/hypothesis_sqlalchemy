from hypothesis import given
from hypothesis.searchstrategy import SearchStrategy
from hypothesis.strategies import DataObject
from sqlalchemy.sql.sqltypes import Enum as EnumType

from hypothesis_sqlalchemy.enums import types_factory
from . import strategies


def test_basic() -> None:
    result = types_factory()

    assert isinstance(result, SearchStrategy)


@given(strategies.data)
def test_enum_types_factory(data: DataObject) -> None:
    strategy = types_factory()

    result = data.draw(strategy)

    assert isinstance(result, EnumType)
