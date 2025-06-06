from baseModel import *
class City(BaseModel):
    id = AutoField(column_name = "id")
    name = CharField(column_name = "name")
    class Meta:
        table_name = "Cities"

    @staticmethod    
    def get_id(city):
        print(city)
        adx = [c.name for c in City.select().where(City.name == city)]
        print(adx)
        if len(adx) == 0:
            adx.append(City.create(name=city))
        return adx[0].id