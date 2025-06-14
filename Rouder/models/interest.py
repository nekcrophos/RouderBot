from baseModel import *
from user import User
from theme import Theme
class Interest(BaseModel):
    id = AutoField(column_name = "id")
    name = CharField(column_name = "name")
    theme_id = ForeignKeyField(Theme)
    class Meta:
        table_name = "Interests"
def textToInt(text):
    if text == 'rock': return 1
    if text == 'electro': return 2
    if text == 'hiphop': return 3
    if text == 'pop': return 4
    if text == 'shanson': return 5
    if text == 'coffee': return 6
    if text == 'wine': return 7
    if text == 'beer': return 8
    if text == 'restaurant': return 9
    if text == 'streetfood': return 10
    if text == 'boardgames': return 11
    if text == 'quizes': return 12
    if text == 'karaoke': return 13
    if text == 'dances': return 14
    if text == 'sports': return 15
    if text == 'cinema': return 16
    if text == 'comics': return 17
    if text == 'anime': return 18
    if text == 'nostalgia': return 19
    if text == 'books': return 20
    if text == 'zoj': return 21
    if text == 'travel': return 22
    if text == 'crypto': return 23
    if text == 'fashion': return 24
    if text == 'ecology': return 25
    return 0