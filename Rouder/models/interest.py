from baseModel import *
from user import User

class Interest(BaseModel):
    id = AutoField(column_name = "id")
    name = CharField(column_name = "name")
    theme_id = ForeignKeyField(Theme)
    class Meta:
        table_name = "Interests"