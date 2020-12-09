import sqlite3
from database import Database
from pathlib import Path
from position_manager import Position

class Storage(Database):
    
    def __init__(self):

        self.__open_connection()

        try:
            create = Path('db_table_creation.txt').read_text()
            self.csr.execute(create)
        except sqlite3.DatabaseError:
            pass

        self.__close_connection()

    def __open_connection(self):
        try:
            self.conn = sqlite3.connect("bot_history.db")
            self.csr = self.conn.cursor()
        except sqlite3.Error as e:
            print("CRITICAL ERROR - DATABASE FAILURE {} {}".format(e.__cause__, e.__traceback__))

    def __close_connection(self):
        try:
            self.csr.close()
            self.conn.close()
        except sqlite3.Error as e:
            print("CRITICAL ERROR - DATABASE FAILURE {} {}".format(e.__cause__, e.__traceback__))

    def tick_history(self) -> list:

        self.__open_connection()

        selector = "SELECT * FROM tick_history"
        self.csr.execute(selector)
        
        hist = []

        for n in len(self.csr.rowcount()):
            row = self.csr.fetchone()
            if row:
                hist.append((row['price'], row['time']))

        self.__close_connection()
        return hist
        

    def close_tick(self):
        pass

    def open_positions(self) -> list:
        pass

    def new_position(self, position : Position):
        pass