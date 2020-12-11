import talib
from threading import Thread, Lock
import numpy as np
from config import config
from slq_lite_database import Storage
from tick_listener import TickListener
from position import Position


class TickManager(TickListener):

    def __init__(self, priceHistory)  -> None:
        self.MA_PERIOD = config['maPeriod']
        self.MA_TYPE = config['maType']
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
                p.notify(tickPrice)
            else:
                self.storage.close_position(p)
                self.positions.remove(p)

        if onClose:
            self.__update(tickPrice)

        self.positionLock.release()

    def __update(self, tickPrice):

        self.tickHistory.append(tickPrice)

        ma = talib.MA(np.array(self.tickHistory), self.MA_PERIOD, self.MA_TYPE)[-1]
        rsi = talib.RSI(np.array(self.tickHistory), self.RSI_PERIOD)[-1]
        upper, middle, lower = talib.BBANDS(np.array(self.tickHistory), self.BB_PERIOD, self.BB_WIDTH, self.BB_WIDTH, self.BB_TYPE)
        print("RSI {}".format(str(rsi))) # DEBUG
        print("Lower BBand {}".format(str(lower[-1]))) # DEBUG
        print("Moving Average {}".format(str(ma))) # DEBUG

        if (rsi < 30) & (tickPrice < lower[-1]):
            self.__enter_position(tickPrice)

        for p in self.positions:
            p.notify_close(tickPrice, ma)

        self.tickHistory = self.tickHistory[-100:]
        
    def __enter_position(self, entryPoint) -> None:
        if len(self.positions) < self.MAX_POSITION_LOAD:
            new_position = Position.create_position(entryPoint, self.SYMBOL)
            self.storage.new_position(new_position)
            self.positions.append(new_position)