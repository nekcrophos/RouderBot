import datetime
from baseModel import BaseModel
from peewee import *

from user import User

class Review(BaseModel):
    id = AutoField(column_name = "id")
    text = CharField(column_name = "text", null = True)
    rating = IntegerField(column_name = "rating")
    user_id = ForeignKeyField(User)
    data = DateTimeField(column_name="date", default=datetime.datetime.now)
    class Meta:
        table_name = "Reviews"
if __name__ == "__main__":
    review = Review(text = "sdsdffasdf",rating = 2,user_id = 1232)
    review.save()
    for review in Review.select().dicts().execute():
        print("review: ", review)