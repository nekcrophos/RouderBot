class User:
    def __init__(self, telegram_id: int, name: str, surname: str, age: int):
        self.telegram_id = telegram_id
        self.name = name
        self.surname = surname
        self.age = age
    def __str__(self):
        return f'User(telegram_id: {self.telegram_id}, name: {self.name}, surname: {self.surname}, age: {self.age})'