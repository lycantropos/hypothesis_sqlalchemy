from hypothesis import strategies

from tests.strategies import (data,
                              max_sizes,
                              metadatas,
                              min_sizes)

data = data
min_sizes = min_sizes
max_sizes = max_sizes
metadatas_strategies = strategies.just(metadatas)
