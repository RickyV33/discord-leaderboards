from discord import Message
from typing import Any

from db.models.channel import Channel
from db.models.game import Game
from db.models.score import Score
from db.models.user import User
from games.game_api import GameApi
from games.game_api_provider import GameApiProvider
from games.game_type import GameType


class ChannelScorer:
    def __init__(
        self,
        *,
        channel_id: str,
        game_db_api: Game,
        score_db_api: Score,
        channel_db_api: Channel,
        game_api_provider: GameApiProvider
    ) -> Any:
        self.channel_id = channel_id
        self.game_api_provider = game_api_provider
        self.game_db_api = game_db_api
        self.score_db_api = score_db_api
        self.channel_db_api = channel_db_api

    def score(self, message: Message) -> int:
        game_api = self.game_api_provider.provide(self._get_game_name())
        if not game_api.is_valid(message.content):
            raise Exception(f"Unable to score message: {message.id}")
        discord_user_id = message.author.id
        channel_id = message.channel.id
        score = game_api.score(message.content)
        round = game_api.round(message.content)
        user_id, _ = User.get_or_create(
            discord_user_id=discord_user_id, discord_name=message.author.name
        )
        channel_id = self.channel_db_api.get(discord_channel_id=channel_id)
        self.score_db_api.insert(
            user=user_id,
            game=self._get_game().id,
            score=score,
            round=round,
            date_submitted=message.created_at,
        ).on_conflict_replace().execute()

        return score

    def get_reaction(self) -> str:
        game_api = self.game_api_provider.provide(self._get_game_name())
        return game_api.get_reaction()

    def _get_game(self) -> Game:
        game_id = self.channel_db_api.get_or_none(self.channel_id).game_id
        game = self.game_db_api.get_or_none(game_id)
        return game

    def _get_game_name(self) -> GameType:
        return GameType(self._get_game().game_name)

    def last_scored_game(self) -> Score:
        result = (
            self.score_db_api.select()
            .join(Game)
            .where(Game.game_name == self._get_game_name().value)
            .order_by(Score.created_at.desc())
            .get()
        )

        return result
