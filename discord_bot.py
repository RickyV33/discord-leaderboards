import discord
from dotenv import dotenv_values

from channels import ChannelScorer, ChannelScorerFetcher

class DiscordBot:
    def __init__(self, *, token: str, channel_scorer_fetcher: ChannelScorerFetcher):
        self.token: str = token
        self.intents: discord.Intents = discord.Intents.all()
        self.client: discord.Client = discord.Client(intents=self.intents)
        self.channel_scorer_fetcher: ChannelScorerFetcher = channel_scorer_fetcher

    def setup_events(self):
        @self.client.event
        async def on_ready():
            print(f'We have logged in as {self.client.user}')

        @self.client.event
        async def on_message(message):
            channel = message.channel
            if self.channel_scorer_fetcher.exists(channel):
                channel_scorer = self.channel_scorer_fetcher.get(channel)
                score = channel_scorer.score(message.content)
                await message.channel.send(f"Scored {score} points!")
            # channel = message.channel
            # game = get_game(channel)
            # user = message.author
            # parse_score(game, user, message)
            # score = message.content
            # print(message)

    def run(self):
        self.setup_events()
        self.client.run(self.token)