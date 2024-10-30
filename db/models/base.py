from peewee import *
from dotenv import dotenv_values

config = dotenv_values(".env") 

class BaseModel(Model):
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        database = SqliteDatabase(config['DB_NAME'])