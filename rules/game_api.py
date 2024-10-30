from abc import ABC

class GameApi(ABC):
    def score(self, message_text: str) -> int:
        pass
