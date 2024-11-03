from typing import Self
from dotenv import dotenv_values
from peewee import Database

config = dotenv_values(".env")


class LeaderboardDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super(LeaderboardDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self, db: Database):
        if not hasattr(self, "initialized"):
            self.db = db
            self.initialized = True

    def __enter__(self):
        self.db.connect(reuse_if_open=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.db.is_closed():
            self.db.close()

    def initialize(self):
        from db.models.channel import Channel
        from db.models.game import Game
        from db.models.score import Score
        from db.models.user import User
        print("Initializing database")
        self.db.create_tables([Game, Channel, User, Score])
        print("Database initialized")
