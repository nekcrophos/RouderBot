from baseModel import *
from user import User

class Meeting(BaseModel):
    id = AutoField(column_name = "id")
    place = IntegerField(column_name = "place")
    owner_id = ForeignKeyField(User, backref = "meetings")
    date = DateField(column_name = "date")
    status = IntegerField(column_name = "status", null = True)
    class Meta:
        table_name = "Meetings"