import json
from discord import Message
from dotenv import dotenv_values
from typing import Any

from db.leaderboard_db import LeaderboardDatabase
from db.models.channel import Channel
from db.models.game import Game
from db.models.score import Score
from db.models.user import User
from bot.discord_settings import DiscordChannelSettings
from games.game_api import GameApi
from games.games import Games


config = dotenv_values(".env")


class ChannelScorer:
    def __init__(
        self,
        *,
        game: Games.FRAMED,
        api: GameApi,
        database: LeaderboardDatabase,
        channel_settings: DiscordChannelSettings,
    ) -> Any:
        self.game: Games = game
        self.api: GameApi = api
        self.database: LeaderboardDatabase = database
        self.channel_settings: DiscordChannelSettings = channel_settings

    def init(self) -> None:
        with self.database:
            print(f"Initializing channels for {self.game}")
            print(f"Channel settings: {self.channel_settings.to_dict()}")
            channel_id, _ = Channel.get_or_create(
                discord_channel_id=self.channel_settings.channel_id,
                discord_instance_id=self.channel_settings.instance_id,
            )
            Game.get_or_create(game_name=self.game.value, channel_id=channel_id)

    def score(self, message: Message) -> int:
        if not self.api.is_valid(message.content):
            raise Exception(f"Unable to score message: {message.id}")
        discord_user_id = message.author.id
        channel_id = message.channel.id
        score = self.api.score(message.content)
        round = self.api.round(message.content)
        with self.database:
            user_id, _ = User.get_or_create(
                discord_user_id=discord_user_id, discord_name=message.author.name
            )
            channel_id = Channel.get(discord_channel_id=channel_id)
            game_id = Game.get(game_name=self.game.value, channel=channel_id)
            Score.insert(
                user=user_id,
                game=game_id,
                score=score,
                round=round,
                date_submitted=message.created_at,
            ).on_conflict_replace().execute()

        return score

    def is_valid(self, content: str) -> bool:
        return self.api.is_valid(content)

    def get_reaction(self) -> str:
        return self.api.get_reaction()

    def get_discord_channel_id(self) -> str:
        return self.channel_settings.channel_id

    def last_scored_game(self) -> Score:
        with self.database:
            result: Score = (
                Score.select()
                .join(Game)
                .where(Game.game_name == self.game.value)
                .order_by(Score.created_at.asc())
                .get()
            )

            return result
