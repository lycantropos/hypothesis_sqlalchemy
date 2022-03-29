from datetime import (date,
                      datetime,
                      timedelta)
from decimal import Decimal
from typing import (Tuple,
                    Union)

from hypothesis.strategies import SearchStrategy

ColumnValue = Union[int, bool, float, Decimal, str, None, date, timedelta,
                    datetime]
Record = Tuple[ColumnValue, ...]
Strategy = SearchStrategy
