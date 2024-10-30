import sqlite3
from dotenv import dotenv_values
from peewee import SqliteDatabase

from channels.channel_scorer import ChannelScorer
from channels.channel_scorer_provider import ChannelScorerProvider
from db.leaderboard_db import LeaderboardDatabase
from discord_bot import DiscordBot
from games.framed_game_api import FramedGameApi
from games.games import Games
from games.rules.game_rule import FramedGameRule

config = dotenv_values(".env")


if __name__ == '__main__':
    sqlite = SqliteDatabase(config["DB_NAME"])
    database = LeaderboardDatabase(sqlite)
    with database:
        database.initialize()

    framed_api = FramedGameApi(rule=FramedGameRule())
    framed_scorer = ChannelScorer(game=Games.FRAMED, database=database, api=framed_api)
    framed_scorer.init(config["DISCORD_FRAMED_CHANNEL_ID"])

    channel_provider = ChannelScorerProvider()
    channel_provider.add(framed_scorer)

    bot = DiscordBot(token=config["DISCORD_TOKEN"], channel_scorer_fetcher=channel_provider)
    bot.run()
