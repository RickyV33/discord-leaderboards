from dotenv import dotenv_values
from peewee import Database

from db.models import Channel, Game, Score, User

class LeaderboardDatabase:

    def __init__(self, db: Database):
        self.db = db

    def __enter__(self):
        self.db.connect()
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
        self._create_tables()