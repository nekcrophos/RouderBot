from baseModel import *
class City(BaseModel):
    id = AutoField(column_name = "id")
    name = CharField(column_name = "name")
    class Meta:
        table_name = "Cities"