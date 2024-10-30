import discord
from dotenv import dotenv_values

from channels.channel_scorer_provider import ChannelScorerProvider


class DiscordBot:
    def __init__(self, *, token: str, channel_scorer_fetcher: ChannelScorerProvider):
        self.token: str = token
        intents: discord.Intents = discord.Intents.all()
        self.client: discord.Client = discord.Client(intents=intents)
        self.channel_scorer_fetcher: ChannelScorerProvider = channel_scorer_fetcher

    def setup_events(self):
        @self.client.event
        async def on_ready():
            print(f'We have logged in as {self.client.user}')

        @self.client.event
        async def on_message(message):
            channel = message.channel
            print(f"Received message in channel {channel}")
            if self.channel_scorer_fetcher.exists(channel):
                channel_scorer = self.channel_scorer_fetcher.get(channel)
                # score = channel_scorer.score(message.content)
                score = 10
                await message.channel.send(f"Scored {score} points!")

    def run(self):
        self.setup_events()
        self.client.run(self.token)