from discord import Message
from bot.commands.base_command import BaseCommand
from db.models.channel import Channel
from games.game_type import GameType


class RegisterCommand(BaseCommand):
    def __init__(
        self,
        game: GameType,
        message: Message,
        channel_db_api: Channel,
    ):
        self.game = game
        self.channel_db_api = channel_db_api
        self.message = message

    def process(self) -> str:
        assert self.message.guild is not None
        _, created = self.channel_db_api.get_or_create(
            discord_channel_id=self.message.channel.id,
            discord_server_id=self.message.guild.id,
            game=self.game.value,
        )
        if created:
            return f"Registered {self.game.value} scoring on this channel"

        return f"{self.game.value} is already registered on this channel"
