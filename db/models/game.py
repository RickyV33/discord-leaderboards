from peewee import AutoField, CharField

from db.models.base import BaseModel


class Game(BaseModel):
    id = AutoField()
    game_name = CharField()
