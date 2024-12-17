from datetime import datetime

import pytz
from db.models.game import Game
from games.game_api import GameApi
from games.game_type import GameType
from games.rules.game_rule import GameRule


class ThriceGameApi(GameApi):
    def __init__(self, *, rule: GameRule, game_db_api: Game) -> None:
        self.rule = rule
        self.game_db_api = game_db_api

    def name(self) -> GameType:
        return GameType(self.rule.name)

    def score(self, message_text: str) -> int:
        return self._get_text_score(message_text)

    def _get_text_score(self, message_text: str) -> int:
        """
        Thrice Game #471 → 6 points.
        """
        return int(message_text.split("→")[1].split("points")[0].strip())

    def _get_emoji_score(self, message_text: str) -> int:
        """
        Thrice Game #471 → 6 points.
        🎲: 3️⃣❌1️⃣2️⃣❌
        www.example.com
        """
        one = "1\ufe0f\u20e3".encode("unicode-escape").decode("ASCII")
        two = "2\ufe0f\u20e3".encode("unicode-escape").decode("ASCII")
        three = "3\ufe0f\u20e3".encode("unicode-escape").decode("ASCII")
        x = "\u274c".encode("unicode-escape").decode("ASCII")
        emoji_text = (
            message_text.split("\n")[1].encode(
                "unicode-escape").decode("ASCII")
        )

        points = {
            x: emoji_text.count(x) * 3,
            one: emoji_text.count(one) * 2,
            two: emoji_text.count(two) * 1,
            three: emoji_text.count(three) * 0,
        }
        return self.rule.max_score - sum(points.values())

    def max_score(self) -> int:
        return self.rule.max_score

    def round(self, message_text: str) -> int:
        """
        Thrice Game #471 → 6 points.
        """
        return int(message_text.split("#")[1].split("→")[0].strip())

    def is_valid(self, message_text: str) -> bool:
        if message_text.count("Thrice Game") != 1:
            return False
        elif message_text.count("🎲") != 1:
            return False
        elif not any(char in message_text for char in self.rule.acceptable_chars):
            return False
        elif self._get_text_score(message_text) != self._get_emoji_score(message_text):
            return False
        elif (
            self.score(message_text) < 0
            or self.score(message_text) > self.rule.max_score
        ):
            return False

        round_grace_period = 1
        if self.round(message_text) > self._current_round() + round_grace_period:
            return False

        return True

    def _current_round(self) -> int:
        game = self.game_db_api.get_or_none(name=self.name().value)
        today_in_pacific: datetime = datetime.now(pytz.timezone("US/Pacific"))
        days_since_anchor = (today_in_pacific.date() - game.date_anchor).days
        current_round = days_since_anchor + game.round_anchor
        return current_round

    def get_reaction(self) -> str:
        return self.rule.reaction_response
