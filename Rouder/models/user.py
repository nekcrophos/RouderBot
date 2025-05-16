class User:
    def __init__(self, telegram_id: int = None, name: str = None, surname: str = None, age: int = 0, avatar: str = None, description: str = None, register = False,  interests = {'music': [], 'place': [], 'actives': [], 'pop_culter': [], 'lifestyle': []}):
        self.avatar = avatar
        self.telegram_id = telegram_id
        self.name = name
        self.surname = surname
        self.description = description
        self.age = age
        self.register = register
        self.interests = interests
    def __str__(self):
        return f'User(telegram_id: {self.telegram_id}, name: {self.name}, surname: {self.surname}, age: {self.age}, description: {self.decription})'