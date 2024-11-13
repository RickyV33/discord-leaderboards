from table2ascii import PresetStyle, table2ascii

from bot.commands.base_command import BaseCommand
from channels.timeframe import Timeframe
from games.game_type import GameType


class HelpCommand(BaseCommand):
    def process(self) -> str:
        commands = table2ascii(
            header=["Command", "Description"],
            body=[
                ["!gooner score <timeframe>", "Get the current scores for all games"],
                ["!gooner <game> score <timeframe>", "Get the current scores"],
                ["!gooner register <game>", "Register a new game"],
                ["!gooner help", "Show this message"],
            ],
            first_col_heading=True,
            style=PresetStyle.thin_rounded,
        )
        timeframe_options = table2ascii(
            header=["Timeframe", "Description"],
            body=[
                [timeframe.value, timeframe.human_readable] for timeframe in Timeframe
            ],
            first_col_heading=True,
            style=PresetStyle.thin_rounded,
        )

        game_options: str = f"Games: {
            ', '.join([game.value for game in GameType])}"
        return f"```{game_options}\n{commands}```\n```{timeframe_options}\n```"
