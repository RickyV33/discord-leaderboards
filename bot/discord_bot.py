import asyncio
from discord import Client, Message
from table2ascii import table2ascii as t2a, PresetStyle

from channels.channel_scorer import ChannelScorer
from channels.channel_scorer_provider import ChannelScorerProvider
from channels.score_fetcher_provider import ScoreFetcherProvider
from channels.timeframe import Timeframe
from channels.total_scores import TotalScores
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
        score_fetcher_provider: ScoreFetcherProvider
    ):
        self.token = token
        self.client: Client = discord_client
        self.channel_scorer_provider: ChannelScorerProvider = channel_scorer_provider
        self.channel_db_api: Channel = channel_db_api
        self.score_fetcher_provider = score_fetcher_provider

    def _build_help_command(self) -> str:
        commands = t2a(
            header=["Command", "Description"],
            body=[
                ["!framed score <timeframe>", "Get the current scores"],
                ["!framed register <game_type>", "Register a new game"],
                ["!framed ping", "Check if the bot is alive"],
                ["!framed help", "Show this message"],
            ],
            first_col_heading=True,
            style=PresetStyle.thin_rounded,
        )
        timeframe_options = t2a(
            header=["Timeframe", "Description"],
            body=[
                [timeframe.value, timeframe.human_readable]
                for timeframe in Timeframe
            ],
            first_col_heading=True,
            style=PresetStyle.thin_rounded,
        )
        return f"```\n{commands}```\n```{timeframe_options}\n```"

    async def _handle_bot_command(self, message: Message):
        commands = message.content.lower().split(" ")
        action = commands[1]
        if action == "ping":
            await message.channel.send("Pong!")
        else:
            await message.channel.send(self._build_help_command())

    async def _handle_game_command(self, message: Message):
        # TODO: this should be handled by another class
        commands = message.content.lower().split(" ")
        action = commands[1] if len(commands) > 1 else None
        if action == "score":
            timeframe = Timeframe(
                commands[2]) if commands[2] else Timeframe.ALL
            discord_channel_id = str(message.channel.id)
            channel = self.channel_db_api.get_or_none(
                discord_channel_id=discord_channel_id)
            response: TotalScores = self.score_fetcher_provider.provide(
                channel.discord_server_id).get(GameType.FRAMED, timeframe)
            await message.channel.send(response.to_discord_message())
        else:
            await message.channel.send(self._build_help_command())

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
                await self._handle_bot_command(message)
            elif message.content.lower().startswith("!framed"):
                await self._handle_game_command(message)
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
            print(f"Backfilling channel: {
                  discord_channel.name}-{channel_id}")  # type: ignore
            chunk_size = 50
            handler: ChannelScorer = self.channel_scorer_provider.provide(
                channel.id)
            last_game = handler.last_scored_game()
            after = None
            if last_game:
                after = discord_channel.get_partial_message(  # type: ignore
                    int(last_game.discord_message_id))  # type: ignore

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
