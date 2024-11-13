import os
from typing import Any
from peewee import Model, SqliteDatabase, DateTimeField, SQL

from db.leaderboard_db import LeaderboardDatabase


class BaseModel(Model):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if "DB_NAME" in os.environ:
            name = os.environ["DB_NAME"]
        else:
            name = "leaderboard.db"
        database = SqliteDatabase(f"sqlite/{name}")
        with LeaderboardDatabase(database):
            return super().__call__(*args, **kwds)

    class Meta:
        if "DB_NAME" in os.environ:
            name = os.environ["DB_NAME"]
        else:
            name = "leaderboard.db"
        database = SqliteDatabase(f"sqlite/{name}")
