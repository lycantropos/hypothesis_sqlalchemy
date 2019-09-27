from typing import Tuple

from hypothesis import strategies
from sqlalchemy.engine import Dialect

from hypothesis_sqlalchemy.hints import Strategy
from hypothesis_sqlalchemy.utils import to_sql_identifiers
from tests.strategies import (data,
                              dialects,
                              max_sizes,
                              metadatas,
                              min_sizes)

data = data
dialects = dialects
just = strategies.just


def to_dialects_with_names(dialect: Dialect) -> Strategy[Tuple[Dialect, str]]:
    return strategies.tuples(just(dialect), to_sql_identifiers(dialect))


dialects_with_names = dialects.flatmap(to_dialects_with_names)
min_sizes = min_sizes
max_sizes = max_sizes
metadatas = metadatas
