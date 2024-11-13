from discord import Message
from bot.commands.base_command import BaseCommand
from bot.commands.help_command import HelpCommand
from bot.commands.register_command import RegisterCommand
from bot.commands.score_command import ScoreCommand
from channels.score_fetcher_provider import ScoreFetcherProvider
from channels.timeframe import Timeframe
from db.models.channel import Channel
from db.models.game import Game
from games.game_type import GameType


class MessageCommandParser:
    def __init__(
        self,
        score_fetcher_provider: ScoreFetcherProvider,
        channel_db_api: Channel,
        game_db_api: Game,
    ):
        self.score_fetcher_provider = score_fetcher_provider
        self.channel_db_api = channel_db_api
        self.game_db_api = game_db_api

    def parse(self, message: Message) -> list[BaseCommand]:
        result = self._parse_message(message)
        if isinstance(result, list):
            return result
        return [result]

    def _parse_message(self, message: Message) -> list[BaseCommand] | BaseCommand:
        commands: list[str] = message.content.lower().split(" ")[1:]
        if len(commands) == 0:
            return self._build_help_command()

        first_command: str = commands[0].lower()
        if first_command == "register":
            return self._register_game(message, commands[1:])
        elif first_command == "score":
            return self._all_scores(message, commands[1:])
        elif first_command.lower() in [game.value for game in GameType]:
            return self._handle_game_command(
                message, GameType(first_command.lower()), commands[1:]
            )
        else:
            return self._build_help_command()

    def _all_scores(self, message: Message, commands: list[str]) -> list[BaseCommand]:
        assert message.guild is not None
        if len(commands) != 1:
            return [self._build_help_command()]

        raw_timeframe = commands[0].lower()
        channels = self.channel_db_api.select().where(
            Channel.discord_channel_id == str(message.channel.id)
        )
        all_scores: list[BaseCommand] = []
        for channel in channels:
            game = GameType(channel.game.name)
            timeframe = (
                Timeframe(raw_timeframe)
                if raw_timeframe in [timeframe.value for timeframe in Timeframe]
                else Timeframe.ALL
            )
            all_scores.append(
                ScoreCommand(
                    game,
                    timeframe,
                    str(message.guild.id),
                    self.score_fetcher_provider,
                )
            )
        return all_scores

    def _register_game(self, message: Message, commands: list[str]) -> BaseCommand:
        if len(commands) != 1:
            return self._build_help_command()

        game = commands[0].lower()
        if game not in [game.value for game in GameType]:
            return self._build_help_command()

        return RegisterCommand(
            GameType(game), message, self.channel_db_api, self.game_db_api
        )

    def _build_help_command(self) -> BaseCommand:
        return HelpCommand()

    def _handle_game_command(
        self, message: Message, game: GameType, commands: list[str]
    ) -> BaseCommand:
        if len(commands) != 2:
            return self._build_help_command()
        action = commands[0].lower()
        if action != "score":
            return self._build_help_command()

        raw_timeframe = commands[1].lower()
        timeframe = (
            Timeframe(raw_timeframe)
            if raw_timeframe in [timeframe.value for timeframe in Timeframe]
            else Timeframe.ALL
        )

        assert message.guild is not None
        return ScoreCommand(
            game,
            Timeframe(timeframe),
            str(message.guild.id),
            self.score_fetcher_provider,
        )
