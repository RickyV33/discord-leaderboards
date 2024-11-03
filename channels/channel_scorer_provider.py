from typing import Any
from channels.channel_scorer import ChannelScorer
from db.models.channel import Channel
from db.models.game import Game
from db.models.score import Score
from games.game_api_provider import GameApiProvider


class ChannelScorerProvider:

    def __init__(
        self,
        game_api_provider: GameApiProvider,
        game_db_api: Game,
        score_db_api: Score,
        channel_db_api: Channel
    ) -> Any:
        self.game_api_provider: GameApiProvider = game_api_provider
        self.game_db_api: Game = game_db_api
        self.score_db_api = score_db_api
        self.channel_db_api = channel_db_api

    def provide(self, channel_id: str) -> ChannelScorer:
        return ChannelScorer(
            channel_id=channel_id,
            game_api_provider=self.game_api_provider,
            game_db_api=self.game_db_api,
            score_db_api=self.score_db_api,
            channel_db_api=self.channel_db_api
        )
