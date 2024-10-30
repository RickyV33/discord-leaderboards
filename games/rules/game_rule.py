from dataclasses import dataclass

from games.games import Games


@dataclass(kw_only=True, frozen=True)
class GameRule:
    name: str
    max_score: int
    acceptable_chars: list[str]


class FramedGameRule(GameRule):
    def __init__(self):
        super().__init__(name=Games.FRAMED, max_score=6, acceptable_chars=["🟥", "🟩", "⬛", "🎥"])