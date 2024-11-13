from discord import Message
from table2ascii import table2ascii, PresetStyle

from channels.timeframe import Timeframe
from channels.total_scores import TotalScores


class MessageCommandParser:

    def parse(self, message: Message):
        if message.content.lower().startswith("!gooner"):
            pass
            # self._handle_bot_command(message)
            # await message.channel.send(self._build_help_command())
        elif message.content.lower().startswith("!framed"):
            self._handle_game_command(message)

    async def _handle_game_command(self, message: Message):
            await message.channel.send(response.to_discord_message())
        else:
            await message.channel.send(self._build_help_command())

    def _build_help_command(self) -> str:
