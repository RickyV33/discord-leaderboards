import json
from peewee import Database

from db.models.channel import Channel
from db.models.game import Game
from db.models.score import Score
from db.models.user import User


class LeaderboardDatabase:

    def __init__(self, db: Database):
        self.db = db

    def __enter__(self):
        self.db.connect(reuse_if_open=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.db.is_closed():
            self.db.close()

    def _validate_connection(self):
        if self.db.is_closed():
            raise ValueError("Database connection is closed")

    def _create_tables(self):
        self.db.create_tables([Game, Channel, User, Score])

    def initialize(self):
        print("Initializing database")
        self._create_tables()
        print("Database initialized")
