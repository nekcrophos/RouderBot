from baseModel import *
from city import City

class User(BaseModel):
    id = AutoField(column_name = "id")
    telegram_id = IntegerField(column_name = "telegram_id", unique = True)
    name = CharField(column_name = "name")
    surname = CharField(column_name = "surname")
    avatar = TextField(column_name = "avatar")
    age = IntegerField(column_name = "age")
    description = TextField(column_name = "description")
    register = BooleanField(column_name = "register")
    city = ForeignKeyField(City, null=True)

    class Meta:
        table_name = "Users"
    def create_new_group(self, name, description = None, theme = None):
        from usersGroup import GroupUsers
        from group import Group
        new_group = Group.create(owner_id = self.telegram_id, name = name, description = description, theme = theme)
        GroupUsers.create(user_id = self.telegram_id, group_id = new_group.id)
        return new_group
    def save_interests(self, themes):
        from interestUser import InterestUser
        from interest import textToInt
        for theme in themes:
            for interest in themes[theme]:
                InterestUser.create(user_id = self.id, interest_id = textToInt(interest))
    def get_interests(self):
        from interest import Interest
        from interestUser import InterestUser
        res = []
        for interest in Interest.select().join(InterestUser).where(InterestUser.user_id == self.id):
            res.append(interest)
        return res
    def get_themes_interests(self):
        interests = {}
        for interest in self.get_interests():
            theme_name = interest.theme_id.name
            if theme_name not in interests:
                interests[theme_name] = []
            interests[theme_name].append(interest.name)
        return interests