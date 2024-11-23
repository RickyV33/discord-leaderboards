from datetime import datetime

import pytz
from db.models.game import Game
from games.game_api import GameApi
from games.game_type import GameType
from games.rules.game_rule import GameRule


class FramedGameApi(GameApi):
    def __init__(self, *, rule: GameRule, game_db_api: Game) -> None:
        self.rule = rule
        self.game_db_api = game_db_api

    def name(self) -> GameType:
        return GameType(self.rule.name)

    def score(self, message_text: str) -> int:
        """
        🎥 🟩 ⬛ ⬛ ⬛ ⬛ ⬛ # 6 points
        🎥 🟥 🟩 ⬛ ⬛ ⬛ ⬛ # 5 points
        🎥 🟥 🟥 🟩 ⬛ ⬛ ⬛ # 4 points
        🎥 🟥 🟥 🟥 🟩 ⬛ ⬛ # 3 points
        🎥 🟥 🟥 🟥 🟥 🟩 ⬛ # 2 points
        🎥 🟥 🟥 🟥 🟥 🟥 🟩 # 1 points
        🎥 🟥 🟥 🟥 🟥 🟥 🟥 # 0 points
        """

        score = self.rule.max_score
        for char in message_text:
            if char in self.rule.acceptable_chars:
                if char == "🟥" or char == "⬛":
                    score -= 1
                elif char == "🟩":
                    break

        return score

    def max_score(self) -> int:
        return self.rule.max_score

    def round(self, message_text: str) -> int:
        """
        Framed #123
        🎥 🟩 ⬛ ⬛ ⬛ ⬛ ⬛
        """
        lines = message_text.splitlines()
        round = int(lines[0].split("#")[1].strip())
        return round

    def is_valid(self, message_text: str) -> bool:
        if message_text.count("Framed") != 1:
            return False
        elif message_text.count("🎥") != 1:
            return False
        elif not any(char in message_text for char in self.rule.acceptable_chars):
            return False
        elif (
            self.score(message_text) < 0
            or self.score(message_text) > self.rule.max_score
        ):
            return False

        round_grace_period = 1
        if self.round(message_text) > self._current_round() + round_grace_period:
            return False

        total_score_chars = 0
        score_chars = ["🟥", "🟩", "⬛"]
        limit = 6
        for char in message_text:
            if total_score_chars > limit:
                return False
            if char in score_chars:
                total_score_chars += 1

        return True

    def _current_round(self) -> int:
        game = self.game_db_api.get_or_none(name=self.name().value)
        today_in_pacific: datetime = datetime.now(pytz.timezone("US/Pacific"))
        days_since_anchor = (today_in_pacific.date() - game.date_anchor).days
        current_round = days_since_anchor + game.round_anchor
        return current_round

    def get_reaction(self) -> str:
        return self.rule.reaction_response
