from discord import Message
from table2ascii import table2ascii, PresetStyle

from bot.commands.base_command import BaseCommand
from bot.commands.score_command import ScoreCommand
from channels.timeframe import Timeframe
from channels.total_scores import TotalScores
from games.game_type import GameType


class MessageCommandParser:
    def parse(self, message: str) -> BaseCommand:
        if message.lower().startswith("!gooner "):
            pass
            # self._handle_bot_command(message)
            # await message.channel.send(self._build_help_command())
        elif message.lower().startswith("!gooner "):
            self._get_commands()

    def _parse_commands(self, message: str) -> BaseCommand:
        commands: list[str] = message.content.lower().split(" ")[1:]
        if len(commands) == 0:
            return self._build_help_command()

        first_command: str = commands[0]
        if first_command == "register":
            return self._register_game_command(commands)
        elif first_command == "list":
            return self._list_games_command()
        elif first_command in [game.value for game in GameType]:
            return self._handle_game_command(GameType(first_command), commands[1:])
        else:
            return self._build_help_command()

    def _handle_game_command(self, game: GameType, commands: list[str]) -> BaseCommand:
        if len(commands) == 0:
            return self._build_help_command()

        first_command = commands[0]
        if first_command == "score":
            return self._get_scores_command(commands[1:])
        else:
            return self._build_help_command()

    def _get_scores_command(self, game: GameType, commands: list[str]) -> BaseCommand:
        if len(commands) == 0:
            return self._build_help_command()

        timeframe = commands[0]
        if timeframe not in [timeframe.value for timeframe in Timeframe]:
            return ScoreCommand()

        return TotalScores(GameType[commands[0]])

    # async def _handle_game_command(self, message: Message):
    #         await message.channel.send(response.to_discord_message())
    # else:
    #     await message.channel.send(self._build_help_command())

    # def _build_help_command(self) -> str:
