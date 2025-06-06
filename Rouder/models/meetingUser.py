from baseModel import *
from group import Group
from user import User

class MeetingUser(BaseModel):
    id = AutoField(column_name = "id")
    user_id = ForeignKeyField(User)
    group_id = ForeignKeyField(Group)
    class Meta:
        table_name = "MeetingUsers"