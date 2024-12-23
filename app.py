import os
import sys
from discord import Client, Intents
from dotenv import load_dotenv
from peewee import SqliteDatabase

from actions import Actions
from bot.command_parser import MessageCommandParser
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
from games.game_type import GameType
from games.rules.game_rule import FramedGameRule, ThriceGameRule
from games.thrice_game_api import ThriceGameApi

load_dotenv()


def main():
    if len(sys.argv) < 2:
        raise ValueError(
            f"Please provide an action to run. Try: {
                [action.value for action in Actions]}"
        )
    action = Actions(sys.argv[1].lower()) or Actions.RUN

    sqlite = SqliteDatabase(f"sqlite/{os.environ["DB_NAME"]}")
    database = LeaderboardDatabase(sqlite)
    framed_api = FramedGameApi(rule=FramedGameRule(), game_db_api=Game)
    thrice_api = ThriceGameApi(rule=ThriceGameRule(), game_db_api=Game)
    game_api_provider = GameApiProvider([framed_api, thrice_api])
    channel_provider = ChannelScorerProvider(
        game_api_provider, Game, Score, Channel, User
    )
    score_fetcher_provider = ScoreFetcherProvider(
        game_api_provider, Game, Score, Channel, User
    )

    token: str = str(os.environ["DISCORD_TOKEN"])
    intents = Intents.all()
    discord_client: Client = Client(intents=intents)
    command_parser: MessageCommandParser = MessageCommandParser(
        score_fetcher_provider=score_fetcher_provider,
        channel_db_api=Channel,
        game_db_api=Game,
    )

    bot = DiscordBot(
        discord_client=discord_client,
        token=token,
        channel_scorer_provider=channel_provider,
        channel_db_api=Channel,
        score_fetcher_provider=score_fetcher_provider,
        command_parser=command_parser,
    )

    if action == Actions.RUN:
        bot.listen()
    elif action == Actions.BACKFILL:
        channel_id = sys.argv[2]
        bot.backfill(channel_id=channel_id)
    elif action == Actions.INIT_DB:
        with database:
            database.initialize()
    elif action == Actions.ADD_GAME:
        if len(sys.argv) != 5:
            raise ValueError("Please provide: game_type, round_anchor, date_anchor")
        game_type = GameType(sys.argv[2].lower())
        round = sys.argv[3]
        round_date = sys.argv[4]
        game, created = Game.get_or_create(
            name=game_type.value, round_anchor=round, date_anchor=round_date
        )
        print(f"Game {game.name} created: {created}")
    else:
        raise ValueError(f"Invalid action: {action}")


if __name__ == "__main__":
    main()
