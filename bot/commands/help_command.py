from table2ascii import PresetStyle, table2ascii

from bot.commands.base_command import BaseCommand
from games.game_type import GameType


class HelpCommand(BaseCommand):
    def process(self):
        commands = table2ascii(
            header=["Command", "Description"],
            body=[
                ["!gooner <game> score <timeframe>", "Get the current scores"],
                ["!gooner register <game>", "Register a new game"],
                ["!gooner list", "List all registered games"],
                ["!gooner help", "Show this message"],
            ],
            first_col_heading=True,
            style=PresetStyle.thin_rounded,
        )
        timeframe_options = table2ascii(
            header=["Timeframe", "Description"],
            body=[
                [timeframe.value, timeframe.human_readable]
                for timeframe in Timeframe
            ],
            first_col_heading=True,
            style=PresetStyle.thin_rounded,
        )

        game_options = table2ascii(
            header=["Game"],
            body=[
                [game.value, game.human_readable]
                for game in GameType
            ],
            first_col_heading=True,
            style=PresetStyle.thin_rounded,
        )
        game_options: str = f"Games: {
            ', '.join([game.value for game in GameType])}"
        return f"```{game_options}\n{commands}```\n```{timeframe_options}\n```"
