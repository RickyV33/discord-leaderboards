from datetime import datetime
from enum import Enum

import pytz


class Timeframe(Enum):
    ALL = "all"
    YEAR = "year"
    SIX_MONTHS = "six_months"
    MONTH = "month"
    WEEK = "week"
    NEW_AGE = "new_age"

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
        elif self == Timeframe.NEW_AGE:
            return datetime.fromisoformat("2024-11-14")
        else:
            raise ValueError(f"Invalid timeframe: {self}")

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
        elif self == Timeframe.NEW_AGE:
            today_in_pacific: datetime = datetime.now(
                pytz.timezone("US/Pacific"))
            delta = today_in_pacific - \
                datetime.fromisoformat(
                    "2024-11-13").replace(tzinfo=pytz.timezone("US/Pacific"))
            return delta.days
        else:
            raise ValueError(f"Invalid timeframe: {self}")

    @property
    def human_readable(self) -> str:
        if self == Timeframe.ALL:
            return "all time"
        elif self == Timeframe.YEAR:
            return "the past year"
        elif self == Timeframe.SIX_MONTHS:
            return "the past six months"
        elif self == Timeframe.MONTH:
            return "the past month"
        elif self == Timeframe.WEEK:
            return "the past week"
        elif self == Timeframe.NEW_AGE:
            return "from the new age Nov 14, 2024 and on"
        else:
            raise ValueError(f"Invalid timeframe: {self}")
