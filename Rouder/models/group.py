from baseModel import *
from user import User
from usersGroup import GroupUsers

class Group(BaseModel):
    id = AutoField(column_name = "id")
    owner_id = ForeignKeyField(User)
    name = CharField(column_name = "name")
    description = CharField(column_name = "description", null = True)
    theme = CharField(column_name = "theme", null = True)
    class Meta:
        table_name = "Groups"
    def addUser(self,user):
        GroupUsers.create(user_id=user.id,group_id=self.id)
    def getMembers(self):
        return GroupUsers.select().where(GroupUsers.group_id == self.id)
        