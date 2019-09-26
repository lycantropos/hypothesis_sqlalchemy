from typing import (List,
                    Tuple)

from hypothesis import given
from sqlalchemy.schema import (Column,
                               UniqueConstraint)

from hypothesis_sqlalchemy.constrained import unique_factory
from hypothesis_sqlalchemy.hints import Strategy
from tests.utils import (Bounds,
                         DataObject)
from . import strategies


@given(strategies.columns_lists_with_bounds)
def test_basic(columns_with_bounds: Tuple[List[Column], Bounds]) -> None:
    columns, (min_size, max_size) = columns_with_bounds

    result = unique_factory(columns,
                            min_size=min_size,
                            max_size=max_size)

    assert isinstance(result, Strategy)


@given(strategies.data, strategies.columns_lists_with_bounds)
def test_examples(data: DataObject,
                  columns_with_bounds: Tuple[List[Column], Bounds]) -> None:
    columns, (min_size, max_size) = columns_with_bounds

    strategy = unique_factory(columns,
                              min_size=min_size,
                              max_size=max_size)

    result = data.draw(strategy)

    assert isinstance(result, UniqueConstraint)
    assert len(result.columns) >= min_size
    assert max_size is None or len(result.columns) <= max_size
    assert all(column in columns
               for column in result.columns)
