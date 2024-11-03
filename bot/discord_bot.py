import asyncio
from datetime import datetime
from discord import Client, Message

from channels.channel_scorer import ChannelScorer
from channels.channel_scorer_provider import ChannelScorerProvider
from db.models.channel import Channel


class DiscordBot:
    def __init__(self, *, token: str, channel_scorer_provider: ChannelScorerProvider, channel_db_api: Channel, discord_client: Client):
        self.token = token
        self.client = discord_client
        self.channel_scorer_provider: ChannelScorerProvider = channel_scorer_provider
        self.channel_db_api: Channel = channel_db_api

    def _handle_command(self, message: Message):
        print(f"Received command: {message.content}")

    async def _handle_scoring(self, message: Message):
        author = message.author
        if author == self.client.user:
            return
        discord_channel_id = str(message.channel.id)
        channel = self.channel_db_api.get_or_none(
            discord_channel_id=discord_channel_id)
        if not channel:
            print(f"Channel not supproted yet: {discord_channel_id}")
            return

        handler: ChannelScorer = self.channel_scorer_provider.provide(
            channel.id)
        try:
            score, is_counted = handler.score(message)
            await self.ack(handler, is_counted, message)
            print(f"Scored message: {message.id} for user {
                  message.author} with score: {score} as counted: {is_counted}")
        except Exception as e:
            if not str(e).startswith("Unable to score message"):
                print(e)

    async def ack(self, handler: ChannelScorer, is_counted: bool, message: Message):
        has_reaction = False
        for reaction in message.reactions:
            is_bot = reaction.me
            if reaction.emoji == handler.get_reaction() and is_bot:
                has_reaction = True
                break
        if has_reaction:
            return
        print(f"Adding reaction to message: {message.id}")
        if is_counted:
            await message.add_reaction(handler.get_reaction())
        else:
            await message.add_reaction("❌")

    def _setup_events(self):
        @self.client.event
        async def on_ready():
            print(f"Listening...")

        @self.client.event
        async def on_message(message: Message):
            if message.content.lower().startswith("!gooner"):
                self._handle_command(message)
            elif message.content.lower().startswith("!framed"):
                self._handle_command(message)
            else:
                await self._handle_scoring(message)

    def listen(self):
        self._setup_events()
        self.client.run(self.token)

    def _setup_backfill_events(self, channel_id: str):
        @self.client.event
        async def on_ready():
            print(f"We have logged in to backfill as {self.client.user}")
            channel = self.channel_db_api.get(channel_id)
            discord_channel = self.client.get_channel(
                int(channel.discord_channel_id))
            print(f"Backfilling channel: {discord_channel.name}-{channel_id}")
            chunk_size = 50
            handler: ChannelScorer = self.channel_scorer_provider.provide(
                channel.id)
            last_game = handler.last_scored_game()
            after = None
            if last_game:
                after = discord_channel.get_partial_message(
                    int(last_game.discord_message_id))  # type: ignore

            total_messages = 0
            print(f"Starting backfill from {
                  after.created_at if after else 'beginning'}")
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
                # 50 requests per second
                one_second = 1
                await asyncio.sleep(one_second)
            print(f"Processed {total_messages} messages")

    def backfill(self, channel_id: str):
        self._setup_backfill_events(channel_id)
        self.client.run(self.token)
