from bot.commands.base_command import BaseCommand
from channels.score_fetcher_provider import ScoreFetcherProvider
from channels.timeframe import Timeframe
from channels.total_scores import TotalScores
from games.game_type import GameType


class ScoreCommand(BaseCommand):
    def __init__(
        self,
        game: GameType,
        timeframe: Timeframe,
        discord_server_id: str,
        score_fetcher_provider: ScoreFetcherProvider,
    ):
        self.game = game
        self.timeframe = timeframe
        self.discord_server_id = discord_server_id
        self.score_fetcher_provider = score_fetcher_provider

    def process(self) -> str:
        response: TotalScores = self.score_fetcher_provider.provide(
            self.discord_server_id
        ).get(self.game, self.timeframe)
        return response.to_discord_message()

    def process_mobile(self) -> str:
        response: TotalScores = self.score_fetcher_provider.provide(
            self.discord_server_id
        ).get(self.game, self.timeframe)
        return response.to_mobile_discord_message()
