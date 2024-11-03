from dataclasses import dataclass

from channels.timeframe import Timeframe
from games.game_type import GameType


@dataclass(kw_only=True, frozen=True)
class UserScore:
    username: str
    completed: int
    scored: int

@dataclass(kw_only=True, frozen=True)
class TotalScores:
    users: list[UserScore]
    total_possible: int
    timeframe: Timeframe
    game: GameType
    with_missing: bool
