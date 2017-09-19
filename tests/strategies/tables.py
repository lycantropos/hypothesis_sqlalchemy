from hypothesis import strategies
from sqlalchemy import MetaData

from hypothesis_sqlalchemy import tables

metadata = MetaData()
tables = tables.factory(metadatas=strategies.just(metadata))
