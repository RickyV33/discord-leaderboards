from peewee import Model, SqliteDatabase, DateTimeField, SQL
from dotenv import dotenv_values

config = dotenv_values(".env")


class BaseModel(Model):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        if "DB_NAME" in config:
            database = SqliteDatabase(config["DB_NAME"])
        else:
            database = SqliteDatabase("leaderboard.db")
