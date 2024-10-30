from peewee import AutoField, CharField

from db.models.base import BaseModel


class Channel(BaseModel):
    id = AutoField()
    discord_channel_id = CharField()
    discord_channel_name = CharField()