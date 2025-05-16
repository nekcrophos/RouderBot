from peewee import *
class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('bot.db')