from peewee import AutoField, DateTimeField, IntegerField, ForeignKeyField, SQL

from db.models.base import BaseModel
from db.models.game import Game
from db.models.user import User


class Score(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="scores")
    game = ForeignKeyField(Game, backref="scores")
    round = IntegerField()
    score = IntegerField()
    date_submitted = DateTimeField()

    class Meta:
        constraints = [SQL("UNIQUE(user_id, game_id, round)")]
