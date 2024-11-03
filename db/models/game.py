from peewee import AutoField, CharField, DateTimeField, IntegerField

from db.models.base import BaseModel


class Game(BaseModel):
    id = AutoField()
    name = CharField()
    # round_anchor = IntegerField()
    # date_anchor = DateTimeField()
