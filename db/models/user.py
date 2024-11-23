from peewee import AutoField, CharField

from db.models.base import BaseModel


class User(BaseModel):
    id = AutoField()
    discord_user_id = CharField()
    discord_name = CharField()
