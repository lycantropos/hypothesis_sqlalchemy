from typing import (Tuple)

from hypothesis import strategies
from sqlalchemy import MetaData
from sqlalchemy.dialects import (mysql,
                                 postgresql,
                                 sqlite)
from sqlalchemy.engine import Dialect
from sqlalchemy.engine.default import DefaultDialect

from hypothesis_sqlalchemy.core.hints import Strategy
from hypothesis_sqlalchemy.core.utils import to_sql_identifiers
from tests.utils import (MAX_MIN_SIZE,
                         MAX_SIZE)

data = strategies.data()
dialects = (strategies.one_of([strategies.builds(dialect)
                               for dialect in [DefaultDialect,
                                               mysql.dialect,
                                               postgresql.dialect,
                                               sqlite.dialect]]))
just = strategies.just


def to_dialects_with_names(dialect: Dialect) -> Strategy[Tuple[Dialect, str]]:
    return strategies.tuples(just(dialect), to_sql_identifiers(dialect))


dialects_with_names = dialects.flatmap(to_dialects_with_names)
min_tables_sizes = strategies.integers(0, MAX_MIN_SIZE)
max_tables_sizes = (strategies.none()
                    | strategies.integers(MAX_MIN_SIZE + 1, MAX_SIZE))
metadatas = strategies.builds(MetaData)
