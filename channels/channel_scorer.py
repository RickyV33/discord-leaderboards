from dotenv import dotenv_values
from typing import Any, TypedDict

from db import LeaderboardDatabase, Game
from rules import GameRuleFetcher, GameRule

config = dotenv_values(".env")

class ChannelScorer:
    def __init__(self, *, channel_name: str, rules: GameRuleFetcher, database: LeaderboardDatabase) -> Any:
        self.channel_name = channel_name
        self.rule: GameRule = rules.get_rules(channel_name)
        self.database = database


    def score(self, message_text: str) -> int:
        pass
    
    def get_game_for_channel(self, channel_id: int) -> TypedDict: # type: ignore
        with self.database as connection:
            connection.cursor.execute("SELECT game_name FROM game WHERE channel_id = ?", (channel_id,))
            game = connection.cursor.fetchone()
            return game
    
    def is_valid(self, message_text: str) -> bool:
        # return self.score(message_text) >= self.rule.threshold
        return True
    
    def initialize(self, game_to_channels: dict[str, int]) -> None:
        with self.database:
            self._create_game_to_channel_mapping(game_to_channels)

    def _create_game_to_channel_mapping(self, game_to_channels: dict[str, int]):
        for game, channel_id in game_to_channels.items():
            Game.create(game_name=game, channel_id=channel_id).save()

