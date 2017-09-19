from datetime import (date,
                      timedelta,
                      datetime)
from decimal import Decimal
from typing import (Union,
                    Tuple)

from hypothesis.searchstrategy import SearchStrategy

ColumnValueType = Union[int, bool,
                        float, Decimal, str, None,
                        date, timedelta, datetime]
RecordType = Tuple[ColumnValueType, ...]
Strategy = SearchStrategy
