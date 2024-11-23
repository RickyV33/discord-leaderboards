from peewee import AutoField, DateTimeField, IntegerField, ForeignKeyField, SQL, CharField

from db.models.base import BaseModel
from db.models.channel import Channel
from db.models.game import Game
from db.models.user import User


class Score(BaseModel):
    id = AutoField()
    round = IntegerField()
    score = IntegerField()
    user = ForeignKeyField(User, backref="scores")
    game = ForeignKeyField(Game, backref="scores")
    channel = ForeignKeyField(Channel, backref="scores")
    discord_message_id = CharField()
    date_submitted = DateTimeField()

    class Meta:
        constraints = [SQL("UNIQUE(user_id, game_id, round)")]
