from abc import ABC

class GameApi(ABC):

    @property
    def name(self) -> str:
        pass

    def score(self, message_text: str) -> int:
        pass

    def is_valid(self, message_text: str) -> bool:
        pass
