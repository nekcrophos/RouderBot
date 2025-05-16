from baseModel import *
from group import Group
from usersGroup import GroupUsers


class User(BaseModel):
    id = AutoField(column_name = "id")
    telegram_id = IntegerField(column_name = "telegram_id", unique = True)
    name = CharField(column_name = "name")
    surname = CharField(column_name = "surname")
    avatar = TextField(column_name = "avatar")
    age = IntegerField(column_name = "age")
    description = TextField(column_name = "description")
    register = BooleanField(column_name = "register")

    class Meta:
        table_name = "Users"
    def create_new_group(self, name, description = None, theme = None):
        new_group = Group.create(owner_id = self.telegram_id, name = name, description = description, theme = theme)
        GroupUsers.create(user_id = self.telegram_id, group_id = new_group.id)
        return new_group
        