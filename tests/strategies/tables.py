from hypothesis import strategies
from sqlalchemy import MetaData

from hypothesis_sqlalchemy.tables import tables_factory

metadata = MetaData()
tables = tables_factory(metadatas=strategies.just(metadata))
