
import talib
from threading import Thread, Lock
import numpy as np
from config import config
from slq_lite_database import Storage
from tick_listener import TickListener
from position import Position


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
        self.positionLock = Lock()
    
    def tick_event(self, tickPrice, closePeriod):
        thread = Thread(target=self.__tick_worker, args=(tickPrice, closePeriod))
        thread.start()

    def __tick_worker(self, tickPrice, onClose):
        print("tick event thread started")
        self.positionLock.acquire()

        for p in self.positions:
            if p.inPosition:
                p.notify(tickPrice, onClose)
            else:
                self.storage.close_position(p)
                self.positions.remove(p)

        self.positionLock.release()

        if onClose:
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
        
        self.tickHistory = self.tickHistory[-50:]
        
    def __enter_position(self, entryPoint) -> None:
        if len(self.positions) < self.MAX_POSITION_LOAD:
            new_position = Position.create_position(entryPoint, self.SYMBOL)
            self.positionLock.acquire()
            self.storage.new_position(new_position)
            self.positions.append(new_position)
            self.positionLock.release()