from operator import attrgetter
from typing import List, Tuple, Optional

from hypothesis import strategies
from sqlalchemy.schema import (Column,
                               MetaData)

from hypothesis_sqlalchemy import tabular
from hypothesis_sqlalchemy.hints import Strategy
from tests.strategies import (data,
                              dialects)
from tests.utils import Bounds

data = data
columns_lists = (dialects
                 .flatmap(lambda dialect:
                          tabular.factory(dialect=dialect,
                                          metadata=MetaData()))
                 .map(attrgetter('columns'))
                 .map(list))


def to_columns_lists_with_bounds(columns: List[Column]
                                 ) -> Strategy[Tuple[List[Column],
                                                     Bounds]]:
    def min_size_to_bounds(min_size: int) -> Strategy[Bounds]:
        return strategies.tuples(strategies.just(min_size),
                                 strategies.none()
                                 | strategies.integers(min_size, len(columns)))

    return strategies.tuples(strategies.just(columns),
                             strategies.integers(0, len(columns))
                             .flatmap(min_size_to_bounds))


columns_lists_with_bounds = columns_lists.flatmap(to_columns_lists_with_bounds)
