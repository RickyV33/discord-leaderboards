from discord import Message
from dotenv import dotenv_values
from typing import Any

from db.leaderboard_db import LeaderboardDatabase
from db.models.game import Game
from games.game_api import GameApi
from games.games import Games 


config = dotenv_values(".env")

class ChannelScorer:
    def __init__(self, *, game: Games.FRAMED, api: GameApi, database: LeaderboardDatabase) -> Any:
        self.game = game
        self.api =  api
        self.database = database

    def init(self, discord_channel_id: int) -> None:
        with self.database:
            Game.create(game_name=self.game, channel_id=discord_channel_id).save()
    
    def score(self, message: Message) -> int:
        if not self.api.is_valid(message.content):
            raise Exception(f"Unable to score message: {message.id}")
        return self.api.score(message.content) 
    
    def is_valid(self, content: str) -> bool:
        return self.api.is_valid(content)

        

