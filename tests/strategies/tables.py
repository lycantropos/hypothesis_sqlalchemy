from operator import attrgetter

from hypothesis import strategies
from sqlalchemy import MetaData

from hypothesis_sqlalchemy import (columns,
                                   tables)

metadata = MetaData()
non_unique_columns = columns.non_primary_keys_factory(
        are_unique=strategies.just(False))
tables_without_unique_columns = tables.factory(
        metadatas=strategies.just(metadata),
        columns_lists=strategies.lists(non_unique_columns,
                                       unique_by=attrgetter('name')))
tables_with_unique_columns = tables.factory(
        metadatas=strategies.just(metadata))
tables = tables_without_unique_columns | tables_with_unique_columns
