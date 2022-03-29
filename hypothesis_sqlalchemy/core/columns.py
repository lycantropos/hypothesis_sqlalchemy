from operator import attrgetter
from typing import (List,
                    Optional)

from hypothesis import strategies
from sqlalchemy import Column

from .hints import Strategy


def lists(columns: Strategy[Column],
          *,
          min_size: int = 0,
          max_size: Optional[int] = None) -> Strategy[List[Column]]:
    return strategies.lists(columns,
                            min_size=min_size,
                            max_size=max_size,
                            unique_by=attrgetter('name'))
