from hypothesis import given
from hypothesis.searchstrategy import SearchStrategy
from sqlalchemy.schema import (MetaData,
                               Table)

from hypothesis_sqlalchemy.tables import factory
from hypothesis_sqlalchemy.utils import is_column_unique
from tests.utils import DataObject
from . import strategies


@given(strategies.metadatas_strategies)
def test_basic(metadatas: SearchStrategy[MetaData]) -> None:
    result = factory(metadatas=metadatas)

    assert isinstance(result, SearchStrategy)


@given(strategies.data, strategies.metadatas_strategies)
def test_examples(data: DataObject,
                  metadatas: SearchStrategy[MetaData]) -> None:
    strategy = factory(metadatas=metadatas)

    result = data.draw(strategy)

    assert isinstance(result, Table)
    assert not all(map(is_column_unique, result.columns))
