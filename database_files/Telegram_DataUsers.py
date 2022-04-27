import sqlite3


class TelegramDB:
    def __init__(self, database_file):
        """Инициализация соединения с Базой Данных"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS telegram_data (id INTEGER PRIMARY KEY AUTOINCREMENT, 
		telegram_id INT NOT NULL, 
		telegram_name TEXT,
		telegram_username TEXT,
		telegram_surname TEXT, 
		connected_date TEXT)""")
        self.connection.commit()

    def select_from_db(self, telegram_id):
        """Делаем SELECT с таблицы telegram_data в поисках наличия пользователя в  нашей БД"""
        try:
            result = self.cursor.execute(
                """SELECT * FROM telegram_data WHERE telegram_id = '{}' """.format(telegram_id))
            return result.fetchone()
        except sqlite3.Error as e:
            print("Error SQLite3 : ", e)

    def insert_into_db(self, telegram_id, telegram_name, telegram_username, telegram_surname, datetime):
        """Делаем INSERT в Таблицу Telegram Users внося данные об пользователе"""
        try:
            self.cursor.execute(
                """INSERT INTO telegram_data (telegram_id, 
                telegram_name, 
                telegram_username, 
                telegram_surname, 
                connected_date) VALUES (?,?,?,?,?)""",
                (telegram_id, telegram_name, telegram_username, telegram_surname, datetime,))
            self.connection.commit()
        except sqlite3.Error as e:
            print("Error SQLite3 : ", e)
