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

        game_options: str = f"Game Options: {
            ', '.join([game.value for game in GameType])}"
        timeframe_options = f"Timeframe Options: {', '.join([timeframe.value for timeframe in Timeframe])}"
        return f"```{game_options}\n{timeframe_options}\n{commands}```\n"
    
    def process_mobile(self) -> str:
        self.process()