from dataclasses import dataclass

from rules import GameApi, GameRule


class FramedGameApi(GameApi):
    def __init__(self, *, rule: GameRule):
        self.rule = rule
    
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
        if message_text.count("🎥") != 1:
            raise Exception("Message must contain exactly one 🎥")

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

