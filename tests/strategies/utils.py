from hypothesis import strategies

data = strategies.data()
MAX_SIZE = 100
# for simplest table with single boolean column
MAX_MIN_SIZE = 2
min_sizes = strategies.integers(0, MAX_MIN_SIZE)
max_sizes = strategies.none() | strategies.integers(MAX_MIN_SIZE + 1, MAX_SIZE)
