import pytest
from sqlalchemy import MetaData
from sqlalchemy.schema import Table

from tests import strategies
from tests.strategies.tables import metadata as raw_metadata
from tests.utils import example


@pytest.fixture(scope='session')
def metadata() -> MetaData:
    return raw_metadata


@pytest.fixture(scope='session')
def table() -> Table:
    return example(strategies.tables)
