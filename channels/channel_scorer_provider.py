from channels.channel_scorer import ChannelScorer
from channels.discord_channel import DiscordChannel
from games.games import Games


class ChannelScorerProvider:
    def __init__(self):
        self.fetcher: dict[str, ChannelScorer] = {}

    def add(self, channel_scorer: ChannelScorer):
        game: Games = channel_scorer.game
        print(f"Adding {game.discord_channel_name} to fetcher")
        self.fetcher[game.discord_channel_name.value] = channel_scorer

    def exists(self, channel_name: str) -> bool:
        channel = DiscordChannel(channel_name)
        return channel.value in self.fetcher

    def get(self, channel_name: str) -> ChannelScorer:
        return self.fetcher[channel_name]