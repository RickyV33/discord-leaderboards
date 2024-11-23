import asyncio
from discord import Client, Message

from bot.command_parser import MessageCommandParser
from bot.commands.base_command import BaseCommand
from channels.channel_scorer import ChannelScorer
from channels.channel_scorer_provider import ChannelScorerProvider
from channels.score_fetcher_provider import ScoreFetcherProvider
from db.models.channel import Channel
from games.game_type import GameType


class DiscordBot:
    def __init__(
        self,
        *,
        token: str,
        channel_scorer_provider: ChannelScorerProvider,
        channel_db_api: Channel,
        discord_client: Client,
        score_fetcher_provider: ScoreFetcherProvider,
        command_parser: MessageCommandParser,
    ):
        self.token = token
        self.client: Client = discord_client
        self.channel_scorer_provider: ChannelScorerProvider = channel_scorer_provider
        self.channel_db_api: Channel = channel_db_api
        self.score_fetcher_provider = score_fetcher_provider
        self.command_parser = command_parser

    async def _handle_scoring(self, message: Message):
        author = message.author
        if author == self.client.user:
            return
        discord_channel_id = str(message.channel.id)
        channel = self.channel_db_api.get_or_none(
            discord_channel_id=discord_channel_id)
        if not channel:
            print(f"Channel not supported yet: {discord_channel_id}")
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

    async def _handle_message(self, message: Message):
        try:
            commands: list[BaseCommand] = self.command_parser.parse(message)
            for_desktop = "desktop" in message.content.lower()
            for command in commands:
                if for_desktop:
                    await message.channel.send(command.process())
                else:
                    await message.channel.send(command.process_mobile())
        except Exception as e:
            print(e)

    def listen_for_messages(self):
        @self.client.event
        async def on_ready():
            print("Listening...")

        @self.client.event
        async def on_message(message: Message):
            mentions_any_game = any(
                game.value in message.content.lower() for game in GameType
            )
            is_bot_command = message.content.lower().startswith("!gooner")

            if is_bot_command:
                await self._handle_message(message)
            elif mentions_any_game:
                await self._handle_scoring(message)

    def listen(self):
        self.listen_for_messages()
        self.client.run(self.token)

    def _setup_backfill_events(self, channel_id: str):
        @self.client.event
        async def on_ready():
            print(f"We have logged in to backfill as {self.client.user}")
            channel = self.channel_db_api.get_by_id(channel_id)
            discord_channel = self.client.get_channel(
                int(channel.discord_channel_id))
            print(f"Backfilling channel: {
                  discord_channel.name}-{channel_id}")  # type: ignore
            chunk_size = 50
            handler: ChannelScorer = self.channel_scorer_provider.provide(
                channel.id)
            last_game = handler.last_scored_game()
            after = None
            if last_game:
                after = discord_channel.get_partial_message(
                    int(last_game.discord_message_id)
                )

            total_messages = 0
            print(f"Starting backfill from {
                  after.created_at if after else 'beginning'}")
            while iterator := discord_channel.history(  # type: ignore
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
