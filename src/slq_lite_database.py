import calendar, sqlite3, time
from os import stat
from database import Database
from pathlib import Path
from position import Position

class Storage(Database):
    
    def __init__(self):

        self.__open_connection()

        try:
            with open('db_setup.sql', 'r') as sql:
                self.csr.executescript(sql.read())
        except sqlite3.OperationalError:
            print("DB already in use")

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

    def open_positions(self) -> list:
        self.__open_connection()

        select = "SELECT * FROM positions where exit_price=NULL"
        self.csr.execute(select)
        
        open = []

        for r in range(self.csr.rowcount):
            row = self.csr.fetchone()
            open.append(Position(row['entry_price'], row['entry_time'], row['ticker_symbol'], row['units']))

        self.__close_connection()
        return open

    def close_position(self, position : Position):

        self.__open_connection()

        update = "UPDATE positions SET exit_time=?, exit_price=? WHERE entry_time=? AND ticker_symbol=?"
        values = (position.entryTime, position.exitPoint, position.entryTime, position.symbol)

        self.csr.execute(update, values)
        self.conn.commit()

        self.__close_connection()


    def new_position(self, position : Position):

        self.__open_connection()

        insert = "INSERT INTO positions VALUES (?, ?, ?, ?, ?, ?)"
        values = (position.entryTime, position.symbol, position.entryPoint, position.units, None, None)

        self.csr.execute(insert, values)
        self.conn.commit()

        self.__close_connection()