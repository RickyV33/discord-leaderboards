from datetime import datetime
from enum import Enum
from typing import Self


class Timeframe(Enum):
    ALL = "all"
    YEAR = "year"
    SIX_MONTHS = "six_months"
    MONTH = "month"
    WEEK = "week"

    @property
    def datetime(self) -> datetime:
        if self == Timeframe.ALL:
            return datetime.fromisoformat("1970-01-01")
        elif self == Timeframe.YEAR:
            return datetime.now().replace(year=datetime.now().year - 1)
        elif self == Timeframe.SIX_MONTHS:
            return datetime.now().replace(month=datetime.now().month - 6)
        elif self == Timeframe.MONTH:
            return datetime.now().replace(day=datetime.now().day - 30)
        elif self == Timeframe.WEEK:
            return datetime.now().replace(day=datetime.now().day - 7)
        else:
            raise ValueError(f"Invalid timeframe: {self}")

    @property
    def to_days(self) -> int:
        if self == Timeframe.ALL:
            return 0
        elif self == Timeframe.YEAR:
            return 365
        elif self == Timeframe.SIX_MONTHS:
            return 180
        elif self == Timeframe.MONTH:
            return 30
        elif self == Timeframe.WEEK:
            return 7
        else:
            raise ValueError(f"Invalid timeframe: {self}")
