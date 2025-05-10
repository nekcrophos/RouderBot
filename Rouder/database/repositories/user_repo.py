import sys


sys.path.insert(1, 'Rouder\database')
# import base
from base import *
sys.path.insert(1, 'Rouder\models')
from user import User

def add_userA(telegram_id: int, name: str, surname: str, age: int) -> bool:
        query = """
        INSERT INTO Users (telegram_id, name, surname, age)
        VALUES (?, ?, ?, ?)
        """
        cursor = DataBase().execute(query, (telegram_id, name, surname, age), commit=True)
        return cursor is not None and cursor.rowcount > 0
def add_user(user: User) -> bool:
    res = add_userA(user.telegram_id, user.name, user.surname, user.age)
    return res
def get_user(telegram_id: int) -> User:
        """Получение пользователя по telegram_id"""
        query = "SELECT * FROM Users WHERE telegram_id = ?"
        cursor = DataBase().execute(query, (telegram_id,))
        if cursor:
            row = cursor.fetchone()
            if row is None: return None
            return User(row['telegram_id'], row['name'], row['surname'], row['age'])
        return None
def update_username(telegram_id: int, new_name: str) -> bool:
        """Обновление username пользователя"""
        query = "UPDATE users SET name = ? WHERE telegram_id = ?"
        cursor = DataBase().execute(query, (new_name, telegram_id), commit=True)
        return cursor is not None and cursor.rowcount > 0
    
def delete_user(telegram_id: int) -> bool:
        """Удаление пользователя"""
        query = "DELETE FROM users WHERE telegram_id = ?"
        cursor = DataBase().execute(query, (telegram_id,), commit=True)
        return cursor is not None and cursor.rowcount > 0

def get_all_users(): #-> List[dict]:
        """Получение всех пользователей"""
        query = "SELECT * FROM users"
        cursor = DataBase().execute(query,"")
        if cursor:
                return [User(row['telegram_id'], row['name'], row['surname'], row['age']) for row in cursor.fetchall()]
        return []
