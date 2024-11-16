from discord import Message
from bot.commands.base_command import BaseCommand
from db.models.channel import Channel
from db.models.game import Game
from games.game_type import GameType


class DeregisterCommand(BaseCommand):
    def __init__(
        self,
        game: GameType,
        message: Message,
        channel_db_api: Channel,
        game_db_api: Game,
    ):
        self.game = game
        self.channel_db_api = channel_db_api
        self.message = message
        self.game_db_api = game_db_api

    def process(self) -> str:
        assert self.message.guild is not None

        game = self.game_db_api.get_or_none(name=self.game.value)
        registered: Channel = self.channel_db_api.get_or_none(
            discord_channel_id=self.message.channel.id,
            discord_server_id=self.message.guild.id,
            game=game,
        )
        if not registered:
            return f"{self.game.value} does not exist on this channel"

        registered.delete_instance()
        return f"{self.game.value} has been removed from the channel"

    def process_mobile(self) -> str:
        return self.process()