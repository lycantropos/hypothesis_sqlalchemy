import uuid
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from enum import Enum

from hypothesis.strategies import SearchStrategy

Scalar = (
    Decimal
    | Enum
    | bool
    | bytes
    | date
    | datetime
    | float
    | int
    | str
    | time
    | timedelta
    | uuid.UUID
    | None
)
Record = tuple[Scalar, ...]
Strategy = SearchStrategy
