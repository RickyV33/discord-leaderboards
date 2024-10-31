from channels.channel_scorer import ChannelScorer
from channels.discord_channel import DiscordChannel
from games.games import Games


class ChannelScorerProvider:
    def __init__(self):
        self.fetcher: dict[str, ChannelScorer] = {}

    def add(self, channel_scorer: ChannelScorer):
        discord_channel_id: str = channel_scorer.get_discord_channel_id()
        self.fetcher[discord_channel_id] = channel_scorer

    def exists(self, discord_channel_id: str) -> bool:
        return discord_channel_id in self.fetcher

    def get(self, discord_channel_id: str) -> ChannelScorer:
        return self.fetcher[discord_channel_id]

    def get_discord_channel_ids(self) -> list[str]:
        return list(self.fetcher.keys())
