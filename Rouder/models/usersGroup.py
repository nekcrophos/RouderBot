from baseModel import BaseModel
from peewee import *

from group import Group
from user import User

class GroupUsers(BaseModel):
    id = AutoField(column_name = "id")
    user_id = ForeignKeyField(User)
    group_id = ForeignKeyField(Group)
    class Meta:
        table_name = "GroupUsers"