from abc import ABC

from games.game_type import GameType


class GameApi(ABC):

    @property
    def name(self) -> GameType:
        raise NotImplementedError

    def score(self, message_text: str) -> int:
        raise NotImplementedError

    def max_score(self) -> int:
        raise NotImplementedError

    def round(self, message_text: str) -> int:
        raise NotImplementedError

    def is_valid(self, message_text: str) -> bool:
        raise NotImplementedError

    def get_reaction(self) -> str:
        raise NotImplementedError
