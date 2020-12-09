
import talib
from config import config
import numpy as np
from tick_listener import TickListener
from position import Position
from slq_lite_database import Storage

class TickManager(TickListener):

    def __init__(self, priceHistory)  -> None:  
        self.RSI_PERIOD = config['rsiPeriod']
        self.BB_PERIOD = config['bBandRange']
        self.BB_WIDTH = config['bBandWidth']
        self.BB_TYPE = config['bBandType']
        self.PERIOD = config['period']
        self.MAX_POSITION_LOAD = config['positionLoad']
        self.SYMBOL = config['tickerSymbol']

        self.storage = Storage()
        self.positions = self.storage.open_positions()
        self.tickHistory = priceHistory

        print(self.tickHistory) # DEBUG

    def close_event(self, tickPrice):
        self.tickHistory.append(tickPrice)
        self.__update(tickPrice)

        print("Closing candle") # DEBUG

    def __update(self, tickPrice):
        self.rsi = talib.RSI(np.array(self.tickHistory), self.RSI_PERIOD)[-1]
        self.upper, self.middle, self.lower = talib.BBANDS(np.array(self.tickHistory), self.BB_PERIOD, self.BB_WIDTH, self.BB_WIDTH, self.BB_TYPE)
        print("RSI " + str(self.rsi)) # DEBUG
        print("Lower BBand " + str(self.lower[-1])) # DEBUG

        if (self.rsi < 30) & (tickPrice < self.lower[-1]):
            self.__enter_position(tickPrice)
        
    def __enter_position(self, entryPoint) -> None:
        if len(self.positions) < self.MAX_POSITION_LOAD:
            new_position = Position.create_position(entryPoint, self.SYMBOL)
            self.storage.new_position(new_position)
            self.positions.append(new_position)

    def tick_event(self, tickPrice):

        for p in self.positions:
            if not p.inPosition:
                self.storage.close_position(p)
                self.positions.remove(p)
            else:
                p.notify(tickPrice)