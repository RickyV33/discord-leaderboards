from enum import Enum

from channels.discord_channel import DiscordChannel


class Games(Enum):
    FRAMED = "Framed"

    @property
    def discord_channel_name(self) -> DiscordChannel:
        if self == Games.FRAMED:
            return DiscordChannel.FRAMED
        
        raise ValueError(f"Unknown game: {self}")
