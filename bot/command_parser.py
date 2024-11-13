
from bot.commands.base_command import BaseCommand
from bot.commands.help_command import HelpCommand
from bot.commands.score_command import ScoreCommand
from channels.score_fetcher_provider import ScoreFetcherProvider
from channels.timeframe import Timeframe
from db.models.channel import Channel
from games.game_type import GameType


class MessageCommandParser:
    def __init__(self, score_fetcher_provider: ScoreFetcherProvider):
        self.score_fetcher_provider = score_fetcher_provider

    def parse(self, channel: Channel, message: str) -> BaseCommand:
        return self._parse_commands(channel, message)

    def _parse_commands(self, channel: Channel, message: str) -> BaseCommand:
        commands: list[str] = message.lower().split(" ")[1:]
        if len(commands) == 0:
            return self._build_help_command()

        first_command: str = commands[0].lower()
        if first_command == "register":
            return self._build_help_command()
        elif first_command == "list":
            return self._build_help_command()
        elif first_command.lower() in [game.value for game in GameType]:
            return self._handle_game_command(
                channel, GameType(first_command.lower()), commands[1:]
            )
        else:
            return self._build_help_command()

    def _build_help_command(self) -> BaseCommand:
        return HelpCommand()

    def _handle_game_command(
        self, channel: Channel, game: GameType, commands: list[str]
    ) -> BaseCommand:
        if len(commands) != 2:
            return self._build_help_command()
        action = commands[0].lower()
        if action != "score":
            return self._build_help_command()

        timeframe = commands[1].lower()
        if timeframe not in [timeframe.value for timeframe in Timeframe]:
            return ScoreCommand(game, Timeframe.ALL, channel, self.score_fetcher_provider)

        return ScoreCommand(game, Timeframe(timeframe), channel, self.score_fetcher_provider)
