from datetime import datetime, timedelta
from discord import Message, Intents, Client

from channels.channel_scorer_provider import ChannelScorerProvider


class DiscordBot:
    def __init__(self, *, token: str, channel_scorer_fetcher: ChannelScorerProvider):
        self.token: str = token
        intents: Intents = Intents.all()
        self.client: Client = Client(intents=intents)
        self.channel_scorer_fetcher: ChannelScorerProvider = channel_scorer_fetcher

    async def _handle_scoring(self, message: Message):
        author = message.author
        if author == self.client.user:
            return
        discord_channel_id = str(message.channel.id)
        if not self.channel_scorer_fetcher.exists(discord_channel_id):
            print(f"Channel not found: {message.channel.id}")
            return
        handler = self.channel_scorer_fetcher.get(discord_channel_id)
        if not handler.is_valid(message.content):
            print(f"Invalid message: {message.id}")
            return
        handler.score(message)
        has_reaction = False
        for reaction in message.reactions:
            is_bot = reaction.me
            if reaction.emoji == handler.get_reaction() and is_bot:
                has_reaction = True
                break
        if has_reaction:
            print(f"Already reacted to message: {message.id}")
            return
        print(f"Adding reaction to message: {message.id}")
        await message.add_reaction(handler.get_reaction())

    def _setup_events(self):
        @self.client.event
        async def on_ready():
            print(f"We have logged in as {self.client.user}")

        @self.client.event
        async def on_message(message: Message):
            await self._handle_scoring(message)

    def run(self):
        self._setup_events()
        self.client.run(self.token)

    def _setup_backfill_events(self):
        @self.client.event
        async def on_ready():
            print(f"We have logged in as {self.client.user}")
            for (
                discord_channel_id
            ) in self.channel_scorer_fetcher.get_discord_channel_ids():
                discord_channel = self.client.get_channel(int(discord_channel_id))
                print(f"Backfilling channel: {discord_channel.name}")
                chunk_size = 100
                handler = self.channel_scorer_fetcher.get(discord_channel_id)
                after: datetime = handler.last_scored_game().created_at

                total_messages = 0
                while iterator := discord_channel.history(
                    limit=chunk_size, after=after, oldest_first=True
                ):
                    messages = [message async for message in iterator]
                    if len(messages) == 0:
                        break
                    total_messages += len(messages)
                    for message in messages:
                        await self._handle_scoring(message)
                    after = messages[-1].created_at
                print(f"Processed {total_messages} messages")

    def backfill(self):
        self._setup_backfill_events()
        self.client.run(self.token)
