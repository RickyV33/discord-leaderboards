from enum import Enum

from channels.discord_channel import DiscordChannel


class Games(Enum):
    FRAMED = "Framed"

    @property
    def discord_channel_name(self) -> DiscordChannel:
        if self == Games.FRAMED:
            return DiscordChannel.PLAYGROUND
        
        raise ValueError(f"Unknown game: {self}")
    
    def from_channel_name(channel_name: str) -> 'Games':
        if channel_name == DiscordChannel.PLAYGROUND.value:
            return Games.FRAMED

        raise ValueError(f"Unknown channel: {channel_name}")
