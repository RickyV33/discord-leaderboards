from dataclasses import dataclass

from games.game_api import GameApi
from games.rules.game_rule import GameRule


class FramedGameApi(GameApi):
    def __init__(self, *, rule: GameRule):
        self.rule = rule

    @property
    def name(self) -> str:
        return self.rule.name

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

        if score > self.rule.max_score:
            raise Exception(f"Score exceeds limit: {score}")
        return score

    def round(self, message_text: str) -> int:
        """
        Framed #123
        🎥 🟩 ⬛ ⬛ ⬛ ⬛ ⬛
        """
        return int(message_text.split("#")[1].strip())

    def is_valid(self, message_text: str) -> bool:
        if message_text.count("🎥") != 1:
            return False

        if not any(char in message_text for char in self.rule.acceptable_chars):
            return False

        if (
            self.score(message_text) < 0
            or self.score(message_text) > self.rule.max_score
        ):
            return False

        return True
