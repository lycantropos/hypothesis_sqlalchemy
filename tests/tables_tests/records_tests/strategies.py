from operator import attrgetter

from hypothesis import strategies

from hypothesis_sqlalchemy import (columns,
                                   tables)
from tests.strategies import (data,
                              max_sizes,
                              metadatas,
                              min_sizes)

data = data
min_sizes = min_sizes
max_sizes = max_sizes
non_unique_columns = columns.non_primary_keys_factory(
        are_unique=strategies.just(False))
tables_without_unique_columns = tables.factory(
        metadatas=metadatas,
        columns_lists=strategies.lists(non_unique_columns,
                                       unique_by=attrgetter('name')))
tables_with_unique_columns = tables.factory(metadatas=metadatas)
tables = tables_without_unique_columns | tables_with_unique_columns
