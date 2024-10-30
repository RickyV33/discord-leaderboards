from peewee import AutoField, CharField, ForeignKeyField

from db.models.base import BaseModel
from db.models.channel import Channel


class Game(BaseModel):
    id = AutoField()
    game_name = CharField()
    channel = ForeignKeyField(Channel, backref='games')