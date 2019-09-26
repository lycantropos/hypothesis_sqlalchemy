from typing import List

from hypothesis import given
from sqlalchemy.schema import (Column,
                               PrimaryKeyConstraint)

from hypothesis_sqlalchemy.constrained import primary_keys_factory
from hypothesis_sqlalchemy.hints import Strategy
from tests.utils import DataObject
from . import strategies


@given(strategies.columns_lists)
def test_basic(columns: List[Column]) -> None:
    result = primary_keys_factory(columns)

    assert isinstance(result, Strategy)


@given(strategies.data, strategies.columns_lists)
def test_examples(data: DataObject,
                  columns: List[Column]) -> None:
    strategy = primary_keys_factory(columns)

    result = data.draw(strategy)

    assert isinstance(result, PrimaryKeyConstraint)
    assert all(column in columns
               for column in result.columns)
