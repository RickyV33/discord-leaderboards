from dataclasses import dataclass

from dotenv import dotenv_values

config = dotenv_values(".env")


@dataclass(frozen=True, kw_only=True)
class DiscordChannelSettings:
    instance_id: str
    channel_id: str

    def to_dict(self):
        return {"instance_id": self.instance_id, "channel_id": self.channel_id}
