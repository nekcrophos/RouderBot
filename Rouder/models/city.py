from baseModel import *
class City(BaseModel):
    id = AutoField(column_name = "id")
    name = CharField(column_name = "name")
    class Meta:
        table_name = "Cities"

    @staticmethod    
    def get_id(city):
        adx = City.get(City.name == city)
        if adx is None:
            adx = City.create(name=city)
        return adx.id