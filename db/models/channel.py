from peewee import ForeignKeyField
from peewee import AutoField, CharField

from db.models.base import BaseModel
from db.models.game import Game


class Channel(BaseModel):
    id = AutoField()
    discord_channel_id = CharField()
    discord_instance_id = CharField()
    game_id = ForeignKeyField(Game, backref="channels")
