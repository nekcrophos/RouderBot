from baseModel import *
from user import User

class Feedback(BaseModel):
    id = AutoField(column_name = "id")
    from_id = ForeignKeyField(User)
    to_id = ForeignKeyField(User)
    like = BooleanField(column_name="like")
    class Meta:
        table_name = "Feedbacks"