from peewee import AutoField, DateTimeField, IntegerField, ForeignKeyField

from db.models import BaseModel, User, Game


class Score(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='scores')
    game = ForeignKeyField(Game, backref='scores')
    score = IntegerField()
    date_submitted = DateTimeField()
