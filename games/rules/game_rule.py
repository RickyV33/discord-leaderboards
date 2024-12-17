from dataclasses import dataclass

from games.game_type import GameType


@dataclass(kw_only=True, frozen=True)
class GameRule:
    name: str
    max_score: int
    acceptable_chars: list[str]
    reaction_response: str


class FramedGameRule(GameRule):
    def __init__(self):
        super().__init__(
            name=GameType.FRAMED,
            max_score=6,
            acceptable_chars=["🟥", "🟩", "⬛", "🎥"],
            reaction_response="🎥",
        )


class ThriceGameRule(GameRule):
    def __init__(self):
        super().__init__(
            name=GameType.THRICE,
            max_score=15,
            acceptable_chars=["🎲", "❌", "1️⃣", "2️⃣", "3️⃣"],
            reaction_response="🎲",
        )
