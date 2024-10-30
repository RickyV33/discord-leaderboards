import sqlite3
from dotenv import dotenv_values
from peewee import SqliteDatabase

from channels.channel_scorer import ChannelScorer
from channels import ChannelScorerFetcher
from db.leaderboard_db import LeaderboardDatabase
from discord_bot import DiscordBot
from rules.game_rule import FramedGameRule, GameRule

config = dotenv_values(".env")

def get_game(channel):
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game WHERE channel_id = ?", (channel.id,))
    game = cursor.fetchone()
    conn.close()
    return game

def parse_score(user, game, content):
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE discord_user_id = ?", (user.id,))
    user = cursor.fetchone()
    cursor.execute("SELECT * FROM game WHERE game_name = ?", (game,))
    game = cursor.fetchone()
    cursor.execute("INSERT INTO score (user_id, game_id, score, date_submitted) VALUES (?, ?, ?, ?)", (user[0], game[0], content, "2020-08-06"))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    framed_rule = FramedGameRule(rule=GameRule("Framed", 6, ["🟥", "🟩", "⬛", "🎥"]))
    sqlite = SqliteDatabase(config["DB_NAME"])
    database = LeaderboardDatabase(sqlite)
    with database:
        database.initialize()
    framed_scorer = ChannelScorer(name="framed", database=database, rules=framed_rule)
    framed_scorer.initialize({ "Framed": config["DISCORD_FRAMED_CHANNEL_ID"] })
    channel_scorer_fetcher = ChannelScorerFetcher()
    channel_scorer_fetcher.add(framed_scorer)
    bot = DiscordBot(token=config["DISCORD_TOKEN"], channel_scorer_fetcher=channel_scorer_fetcher)
    bot.run()
