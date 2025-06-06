import sqlite3
import sys
# from Rouder.models.baseModel import *
# from Rouder.database.base import *
# from Rouder.database.repositories.user_repo import *
# from Rouder.models.user import User
# Подключаемся к БД (файл создастся автоматически)
conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Cities (
 Id INTEGER PRIMARY KEY AUTOINCREMENT,
 name NVARCHAR(100)
)
''')
conn.commit()
conn.close()
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
 avatar VARCHAR(50),
 register BOOL,
 city INTEGER,
 FOREIGN KEY (city) REFERENCES Cities (id) ON DELETE CASCADE
)
''')
conn.commit()
conn.close()
conn = sqlite3.connect('bot.db')
cursor = conn.cursor()
s = cursor.execute('''
SELECT * FROM Users
''').fetchall()
# for u in s:
#     print(u)
# s = cursor.execute('''
# INSERT INTO Users (telegram_id, name, surname, age)
# VALUES (123436, 'Test_name', 'test_surname', 27)
# ''')
conn.commit()
conn.close()
print('sas')
conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Reviews (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 text NVARCHAR(300),
 rating INT,
 user_id INTEGER NOT NULL,
 data TIMESTAMP
)
''')
conn.commit()
conn.close()
conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS GroupUsers (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 group_id INTEGER,
 user_id INTEGER,
 FOREIGN KEY (group_id) REFERENCES Groups (id) ON DELETE CASCADE,
 FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE
)
''')
conn.commit()
conn.close()

conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Groups (
  id integer PRIMARY KEY AUTOINCREMENT,
  owner_id integer NOT NULL,
  name varchar(255) NOT NULL,
  description varchar(255),
  theme string,
  FOREIGN KEY (owner_id) REFERENCES Users (id) ON DELETE CASCADE
)
''')
conn.commit()
conn.close()
conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Meetings (
  id integer PRIMARY KEY AUTOINCREMENT,
  place varchar(255) NOT NULL,
  owner_id integer NOT NULL,
  date datetime,
  status varchar(255),
  FOREIGN KEY (owner_id) REFERENCES Users (id) ON DELETE CASCADE
)
''')
conn.commit()
conn.close()
conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS MeetingUsers (
  id integer PRIMARY KEY AUTOINCREMENT,
  user_id integer NOT NULL,
  meeting_id integer NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE,
  FOREIGN KEY (meeting_id) REFERENCES Meetings (id) ON DELETE CASCADE
)
''')
conn.commit()
conn.close()

conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Themes(
  id integer PRIMARY KEY AUTOINCREMENT,
  name nvarchar(255) NOT NULL
)
''')
conn.commit()
conn.close()

conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Interests (
  id integer PRIMARY KEY AUTOINCREMENT,
  name nvarchar(255) NOT NULL,
  theme_id integer NOT NULL,
  FOREIGN KEY (theme_id) REFERENCES Themes (id) ON DELETE CASCADE
)
''')
conn.commit()
conn.close()
conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS InterestUsers(
  id integer PRIMARY KEY AUTOINCREMENT,
  interest_id integer NOT NULL,
  user_id integer NOT NULL,
  FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE,
  FOREIGN KEY (interest_id) REFERENCES Interests (id) ON DELETE CASCADE
)
''')
conn.commit()
conn.close()

conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
INSERT INTO Themes(name)
VALUES
('music'),
('place'),
('actives'),
('culter'),
('lifestyle');
''')
conn.commit()
conn.close()
conn = sqlite3.connect('bot.db')  
cursor = conn.cursor()
cursor.execute('''
INSERT INTO Interests(name, theme_id)
VALUES
('rock', 1),
('electro', 1),
('hiphop', 1),
('pop', 1),
('shanson', 1),
('coffee', 2),
('wine', 2),
('beer', 2),
('restaurant', 2),
('streetfood', 2),
('boardgames', 3),
('quizes', 3),
('karaoke', 3),
('dances', 3),
('sports', 3),
('cinema', 4),
('comics', 4),
('anime', 4),
('nostalgia', 4),
('books', 4),
('zoj', 5),
('travel', 5),
('crypto', 5),
('fashion', 5),
('ecology', 5);
''')
conn.commit()
conn.close()