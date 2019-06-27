from hypothesis import strategies

from tests.strategies import (data,
                              metadatas)

data = data
metadatas_strategies = strategies.just(metadatas)
