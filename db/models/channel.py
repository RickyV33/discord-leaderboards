from peewee import ForeignKeyField
from peewee import AutoField, CharField

from db.models.base import BaseModel
from db.models.game import Game


class Channel(BaseModel):
    id = AutoField()
    discord_channel_id = CharField()
    discord_server_id = CharField()
    game = ForeignKeyField(Game, backref="channels")
