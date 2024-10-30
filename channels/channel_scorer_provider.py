from channels.channel_scorer import ChannelScorer
from games.games import Games


class ChannelScorerProvider:
    def __init__(self):
        self.fetcher: dict[str, ChannelScorer] = {}

    def add(self, channel_scorer: ChannelScorer):
        game: Games = channel_scorer.game
        self.fetcher[game.discord_channel_name] = channel_scorer

    def exists(self, channel_name: str) -> bool:
        return channel_name in self.fetcher

    def get(self, channel_name: str) -> ChannelScorer:
        return self.fetcher[channel_name]