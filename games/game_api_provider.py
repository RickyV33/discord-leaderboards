from db.models.channel import Channel
from games.game_api import GameApi
from games.game_type import GameType


class GameApiProvider:
    def __init__(self, game_apis: list[GameApi]) -> None:
        self.game_apis: dict[GameType, GameApi] = {
            game_api.name: game_api
            for game_api in game_apis
        }

    def provide(self, game: GameType) -> GameApi:
        return self.game_apis[game]
