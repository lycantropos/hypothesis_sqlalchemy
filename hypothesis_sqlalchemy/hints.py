from datetime import (date,
                      datetime,
                      timedelta)
from decimal import Decimal
from typing import (Tuple,
                    Union)

from hypothesis.searchstrategy import SearchStrategy

ColumnValueType = Union[int, bool,
                        float, Decimal, str, None,
                        date, timedelta, datetime]
RecordType = Tuple[ColumnValueType, ...]
Strategy = SearchStrategy
