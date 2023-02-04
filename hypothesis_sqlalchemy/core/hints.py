from datetime import (date,
                      datetime,
                      time,
                      timedelta)
from decimal import Decimal
from enum import Enum
from typing import (Tuple,
                    Union)

from hypothesis.strategies import SearchStrategy

Scalar = Union[
    Decimal, Enum, None, bool, date, datetime, float, int, str, time, timedelta
]
Record = Tuple[Scalar, ...]
Strategy = SearchStrategy
