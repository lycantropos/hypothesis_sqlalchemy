from hypothesis import strategies
from sqlalchemy import MetaData

metadatas = strategies.builds(MetaData)
