import pytest
from sqlalchemy.schema import (MetaData,
                               Table)

from tests import strategies
from tests.strategies.tables import metadata as raw_metadata
from tests.utils import example


@pytest.fixture(scope='session')
def metadata() -> MetaData:
    return raw_metadata


@pytest.fixture(scope='function')
def table() -> Table:
    return example(strategies.tables)
