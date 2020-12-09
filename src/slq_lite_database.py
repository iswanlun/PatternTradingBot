import calendar, sqlite3, time
from os import stat
from database import Database
from pathlib import Path
from position_manager import Position

class Storage(Database):
    
    def __init__(self):

        self.__open_connection()

        try:
            create = Path('db_table_creation.txt').read_text()
            self.csr.executescript(create)
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

    def open_positions(self) -> list:
        self.__open_connection()

        select = "SELECT * FROM positions where exit_price=NULL"
        self.csr.execute(select)
        
        open = []

        for n in len(self.csr.rowcount()):
            entryPoint = self.csr.fetchone()['entry_price']
            open.append(Position(entryPoint))

        self.__close_connection()
        return open

    def close_position(position : Position):
        timeStamp = str(calendar.timegm(time.gmtime()))
        pass

    def new_position(self, position : Position):

        self.__open_connection()



        timeStamp = str(calendar.timegm(time.gmtime()))

        self.__close_connection()