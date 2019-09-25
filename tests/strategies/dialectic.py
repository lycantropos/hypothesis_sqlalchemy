from hypothesis import strategies
from sqlalchemy.dialects import (mysql,
                                 postgresql,
                                 sqlite)

from hypothesis_sqlalchemy import dialectic

dialects = (strategies.just(dialectic.default)
            | strategies.one_of([strategies.builds(dialect)
                                 for dialect in (mysql.dialect,
                                                 postgresql.dialect,
                                                 sqlite.dialect)]))
