import sqlite3


class XboxDB:
    def __init__(self, database_file):
        """Инициализация соединения с Базой Данных"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS store_regions (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        country  STRING  UNIQUE,
        address  STRING  UNIQUE,
        city     STRING  UNIQUE,
        region   STRING  UNIQUE,
        postcode STRING  UNIQUE)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS deals (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        deal_name STRING  NOT NULL UNIQUE)""")

        self.connection.commit()

    def select_store_regions(self):
        try:
            result = self.cursor.execute("""SELECT country FROM store_regions""")
            return result.fetchall()
        except sqlite3.Error as e:
            print("Error SQLite3 : ", e)

    def select_details_regions(self, country):
        try:
            result = self.cursor.execute("""SELECT address, city, region, postcode FROM store_regions WHERE country = '{}' """.format(country))
            return result.fetchall()
        except sqlite3.Error as e:
            print("Error SQLite3 : ", e)

    def select_deals_details(self):
        try:
            result = self.cursor.execute("""SELECT deal_name FROM deals""")
            return result.fetchall()
        except sqlite3.Error as e:
            print("Error SQLite3 : ", e)

    def insert_deals_details(self, deal_name):
        try:
            self.cursor.execute("""INSERT INTO deals (deal_name) VALUES (?)""", (deal_name,))
            self.connection.commit()
        except sqlite3.Error as e:
            print("Error SQLite3 : ", e)