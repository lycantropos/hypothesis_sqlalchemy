from operator import attrgetter

from sqlalchemy import MetaData

from hypothesis_sqlalchemy import tabular
from tests.strategies import (data,
                              dialects)

data = data
columns_lists = (dialects
                 .flatmap(lambda dialect:
                          tabular.factory(dialect=dialect,
                                          metadata=MetaData()))
                 .map(attrgetter('columns'))
                 .map(list))
