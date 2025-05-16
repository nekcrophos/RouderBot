from baseModel import *
from interest import Interest
from user import User

class InterestUser(BaseModel):
    id = AutoField(column_name = "id")
    interest_id = ForeignKeyField(Interest)
    user_id = ForeignKeyField(User)
    class Meta:
        table_name = "InterestsUser"