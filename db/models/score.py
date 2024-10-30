from peewee import AutoField, DateTimeField, IntegerField, ForeignKeyField

from db.models.base import BaseModel
from db.models.game import Game
from db.models.user import User



class Score(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='scores')
    game = ForeignKeyField(Game, backref='scores')
    score = IntegerField()
    date_submitted = DateTimeField()
