import sqlite3
import sys
from Rouder.database.base import *
from Rouder.database.repositories.user_repo import *
from Rouder.models.user import User
# Подключаемся к БД (файл создастся автоматически)
conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
 Id INTEGER PRIMARY KEY AUTOINCREMENT,
 telegram_id INTEGER UNIQUE,
 name NVARCHAR(15),
 surname VARCHAR(40),
 age INT,
 description VARCHAR(200),
 avatar VARCHAR(50)
)
''')
conn.commit()
conn.close()
conn = sqlite3.connect('bot.db')
cursor = conn.cursor()
s = cursor.execute('''
SELECT * FROM Users
''').fetchall()
for u in s:
    print(u)
# s = cursor.execute('''
# INSERT INTO Users (telegram_id, name, surname, age)
# VALUES (123436, 'Test_name', 'test_surname', 27)
# ''')
conn.commit()
conn.close()
print('sas')
k = get_all_users()
print('users')
for us in k:
    print(us)