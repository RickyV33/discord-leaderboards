from discord import Message, Intents, Client

from channels.channel_scorer_provider import ChannelScorerProvider


class DiscordBot:
    def __init__(self, *, token: str, channel_scorer_fetcher: ChannelScorerProvider):
        self.token: str = token
        intents: Intents = Intents.all()
        self.client: Client = Client(intents=intents)
        self.channel_scorer_fetcher: ChannelScorerProvider = channel_scorer_fetcher

    def setup_events(self):
        @self.client.event
        async def on_ready():
            print(f"We have logged in as {self.client.user}")

        @self.client.event
        async def on_message(message: Message):
            author = message.author
            if author == self.client.user:
                return
            if not self.channel_scorer_fetcher.exists(message.channel.name):
                return
            handler = self.channel_scorer_fetcher.get(message.channel.name)
            if not handler.is_valid(message.content):
                return
            handler.score(message)
            has_reaction = False
            for reaction in message.reactions:
                is_bot = reaction.me
                if reaction.emoji == handler.get_reaction() and is_bot:
                    has_reaction = True
                    break
            if not has_reaction:
                await message.add_reaction(handler.get_reaction())

    def run(self):
        self.setup_events()
        self.client.run(self.token)
