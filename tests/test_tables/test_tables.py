from hypothesis import strategies
from sqlalchemy.schema import (MetaData,
                               Table)

from hypothesis_sqlalchemy.tables import factory
from hypothesis_sqlalchemy.utils import is_column_unique
from tests.utils import example


def test_tables_factory(metadata: MetaData) -> None:
    tables = factory(metadatas=strategies.just(metadata))
    table = example(tables)

    assert isinstance(table, Table)
    assert any(not is_column_unique(column)
               for column in table.columns)
