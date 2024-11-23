from abc import ABC, abstractmethod

from games.game_type import GameType


class GameApi(ABC):
    @abstractmethod
    def name(self) -> GameType:
        raise NotImplementedError

    @abstractmethod
    def score(self, message_text: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def max_score(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def round(self, message_text: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def is_valid(self, message_text: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_reaction(self) -> str:
        raise NotImplementedError
