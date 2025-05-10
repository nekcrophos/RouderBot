import sqlite3
from sqlite3 import Error
from typing import List, Optional
class _SingletonWrapper:
    """
    Класс-обeртка для реализации паттерна Одиночка.
    """
    def __init__(self, cls):
        self.__wrapped__ = cls  # Оригинальный класс
        self._instance = None   # Здесь будет храниться экземпляр класса
    def __call__(self, *args, **kwargs):
        """Возвращает единственный экземпляр класса"""
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)
        return self._instance
def singleton(cls):
    """
    Декоратор для класса, реализующий синглтон.
    """
    return _SingletonWrapper(cls)
@singleton
class DataBase:
    """Класс для работы с SQLite базой данных"""
    
    def __init__(self, db_file: str = "bot.db"):
            self.db_file = db_file
            self.connection = None
        
        
    
    def __enter__(self):
        """Поддержка контекстного менеджера (with)"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие соединения при выходе из контекста"""
        self.close()
    
    def connect(self) -> None:
        """Установка соединения с базой данных"""
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.connection.execute("PRAGMA foreign_keys = ON")  # Включение внешних ключей
            self.connection.row_factory = sqlite3.Row
            print(f"Успешное подключение к SQLite DB '{self.db_file}'")
        except Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise
    
    def close(self) -> None:
        """Закрытие соединения с базой данных"""
        if self.connection:
            self.connection.close()
            print("Соединение с SQLite закрыто")
    
    def execute(self, query: str, params: any, commit: bool = False):
        """
        Выполнение SQL-запроса
        :param query: SQL-запрос
        :param params: Параметры для запроса
        :param commit: Нужно ли делать commit после выполнения
        :return: Курсор с результатами или None при ошибке
        """
        try:
            if self.connection is None:
                raise Exception("Connection is None")
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            if commit:
                self.connection.commit()
            return cursor
        except Error as e:
            print(f"Ошибка выполнения запроса '{query}': {e}")
            return None