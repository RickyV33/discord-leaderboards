from peewee import AutoField, CharField, ForeignKeyField

from db.models import BaseModel, Channel


class Game(BaseModel):
    id = AutoField()
    game_name = CharField()
    channel = ForeignKeyField(Channel, backref='games')