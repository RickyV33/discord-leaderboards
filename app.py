import sys
from discord import Client, Intents
from dotenv import dotenv_values
from peewee import SqliteDatabase

from actions import Actions
from channels.channel_scorer_provider import ChannelScorerProvider
from channels.score_fetcher_provider import ScoreFetcherProvider
from db.leaderboard_db import LeaderboardDatabase
from bot.discord_bot import DiscordBot
from db.models.channel import Channel
from db.models.game import Game
from db.models.score import Score
from db.models.user import User
from games.framed_game_api import FramedGameApi
from games.game_api_provider import GameApiProvider
from games.rules.game_rule import FramedGameRule

config = dotenv_values(".env")


def main():
    # if len(sys.argv) < 2:
    #     raise ValueError(
    #         f"Please provide an action to run. Try: {
    #             [action.value for action in Actions]}"
    #     )
    action = Actions(sys.argv[1]) or Actions.RUN

    sqlite = SqliteDatabase(config["DB_NAME"])
    database = LeaderboardDatabase(sqlite)
    framed_api = FramedGameApi(rule=FramedGameRule())
    game_api_provider = GameApiProvider([framed_api])
    channel_provider = ChannelScorerProvider(
        game_api_provider, Game, Score, Channel, User)
    score_fetcher_provider = ScoreFetcherProvider(
        game_api_provider, Game, Score, Channel, User)

    token: str = str(config["DISCORD_TOKEN"])
    intents = Intents.all()
    discord_client: Client = Client(intents=intents)

    bot = DiscordBot(
        discord_client=discord_client,
        token=token,
        channel_scorer_provider=channel_provider,
        channel_db_api=Channel,
        score_fetcher_provider=score_fetcher_provider
    )

    if action == Actions.RUN:
        bot.listen()
    elif action == Actions.BACKFILL:
        channel_id = sys.argv[2]
        bot.backfill(channel_id=channel_id)
    elif action == Actions.INIT_DB:
        with database:
            database.initialize()
    else:
        raise ValueError(f"Invalid action: {action}")


if __name__ == "__main__":
    main()
