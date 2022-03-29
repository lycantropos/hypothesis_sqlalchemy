from hypothesis import strategies
from sqlalchemy.dialects import (mysql,
                                 postgresql,
                                 sqlite)
from sqlalchemy.engine.default import DefaultDialect

dialects = (strategies.builds(DefaultDialect)
            | strategies.one_of([strategies.builds(dialect)
                                 for dialect in (mysql.dialect,
                                                 postgresql.dialect,
                                                 sqlite.dialect)]))
