from typing import Any
from channels.channel_scorer import ChannelScorer
from channels.score_fetcher import ScoreFetcher
from db.models.channel import Channel
from db.models.game import Game
from db.models.score import Score
from db.models.user import User
from games.game_api_provider import GameApiProvider


class ScoreFetcherProvider:
    def __init__(
        self,
        game_api_provider: GameApiProvider,
        game_db_api: Game,
        score_db_api: Score,
        channel_db_api: Channel,
        user_db_api: User
    ) -> None:
        self.game_api_provider: GameApiProvider = game_api_provider
        self.game_db_api: Game = game_db_api
        self.score_db_api = score_db_api
        self.channel_db_api = channel_db_api
        self.user_db_api = user_db_api

    def provide(self, server_id: str) -> ScoreFetcher:
        return ScoreFetcher(
            server_id=server_id,
            game_api_provider=self.game_api_provider,
            game_db_api=self.game_db_api,
            score_db_api=self.score_db_api,
            user_db_api=self.user_db_api,
            channel_db_api=self.channel_db_api
        )
