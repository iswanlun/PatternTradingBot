
import mysql.connector
from mysql.connector import errorcode
from src.config import config

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html

class Database:

    def __init__(self):
        pass

    # returns an array of tuples containing data on held positions

    def load_current_positions(self, product):
        self.get_connection()

        arr = []

        query = ("SELECT TradeID, Unit_price, Units, Trade_time FROM "
                "trade_log t, current_positions c WHERE t.TradeID = c.TradeID AND c.In_position = 1 AND Product = %s")
        try:
            self.cursor.execute(query, (product)) # might need (product)
        except BaseException as err:
            self.close_connection()
            print("Could not read data from the db at Database -> load_current_positions")
            print(err)
        
        if self.cursor.rowcount != -1: # indicates an error
            for (TradeID, Unit_price, Units, Trade_time) in self.cursor:
                arr.append((TradeID, Unit_price, Units, Trade_time))

        self.close_connection()

        return arr

    # for one trade data is an array in the format : [TradeID, Product, Unit_price, Units, Trade_type, Trade_time]
    def record_trade(self, data):
        self.get_connection()

        add_trade = ("INSERT INTO trade_log VALUES %s %s %s %s %s %s")
        trade_data = (x for x in data)

        self.cursor.execute(add_trade, trade_data)

        if (data[4] == 'BUY'):
            add_position = ("INSERT INTO current_positions VALUES %s %s")
            position_data = (data[0], 1)
            self.cursor.execute(add_position, position_data)
        
        if (data[4] == 'SELL'):
            change_position = ("UPDATE current_positions SET In_position = 0 WHERE TradeID = %s")
            trade_id = data[0]
            self.cursor.execute(change_position, trade_id)

        self.conn.commit()

        self.close_connection()

        pass

    def get_connection(self):
        try:
            self.conn = mysql.connector.connect(**self.config) # C overlap
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print("Error connecting to database at Database -> get_connection")
            print(err)

    def close_connection(self):
        try:
            self.cursor.close()
            self.conn.close()
        except mysql.connector.Error as err:
            print("Error closing the db connection at Database -> close_connection")
            print(err)