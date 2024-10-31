import sys
from dotenv import dotenv_values
from peewee import SqliteDatabase

from actions import Actions
from channels.channel_scorer import ChannelScorer
from channels.channel_scorer_provider import ChannelScorerProvider
from db.leaderboard_db import LeaderboardDatabase
from bot.discord_bot import DiscordBot
from bot.discord_settings import DiscordChannelSettings
from games.framed_game_api import FramedGameApi
from games.games import Games
from games.rules.game_rule import FramedGameRule

config = dotenv_values(".env")


if __name__ == "__main__":
    if config["ENV"] == "dev":
        action = Actions.RUN
    else:
        if len(sys.argv) != 2:
            raise ValueError(
                f"Please provide an action to run. Try: {[action.value for action in Actions]}"
            )
        action = Actions(sys.argv[1])

    sqlite = SqliteDatabase(config["DB_NAME"])
    database = LeaderboardDatabase(sqlite)
    framed_api = FramedGameApi(rule=FramedGameRule())
    framed_channel = DiscordChannelSettings(
        instance_id=config["DISCORD_INSTANCE_ID"],
        channel_id=config["DISCORD_PLAYGROUND_CHANNEL_ID"],
    )
    framed_scorer = ChannelScorer(
        game=Games.FRAMED,
        database=database,
        api=framed_api,
        channel_settings=framed_channel,
    )
    channel_provider = ChannelScorerProvider()
    channel_provider.add(framed_scorer)
    bot = DiscordBot(
        token=config["DISCORD_TOKEN"], channel_scorer_fetcher=channel_provider
    )

    if action == Actions.RUN:
        bot.run()
    elif action == Actions.BACKFILL:
        pass
    elif action == Actions.INIT_DB:
        with database:
            database.initialize()
    elif action == Actions.INIT_CHANNELS:
        framed_scorer.init()
    else:
        raise ValueError(f"Invalid action: {action}")
