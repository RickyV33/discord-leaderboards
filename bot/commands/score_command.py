from abc import ABC, abstractmethod

from table2ascii import PresetStyle, table2ascii

from bot.commands.base_command import BaseCommand
from channels.score_fetcher_provider import ScoreFetcherProvider
from channels.timeframe import Timeframe
from channels.total_scores import TotalScores
from db.models.channel import Channel
from games.game_type import GameType


class ScoreCommand(BaseCommand):
    def __init__(
        self,
        timeframe: Timeframe,
        channel: Channel,
        score_fetcher_provider: ScoreFetcherProvider,
    ):
        self.message = message
        self.channel = channel
        self.score_fetcher_provider = score_fetcher_provider

    def process(self) -> str:
        commands = self.message.content.lower().split(" ")
        timeframe = Timeframe(commands[2]) if commands[2] else Timeframe.ALL
        response: TotalScores = self.score_fetcher_provider.provide(
            self.channel.discord_server_id
        ).get(GameType.FRAMED, timeframe)
