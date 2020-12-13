
from threading import Thread, Lock
from config import config
from slq_lite_database import Storage
from tick_listener import TickListener
from position import Position
from trade_algorithm import TradeAlgorithm


class TickManager(TickListener):

    def __init__(self, priceHistory)  -> None:
        
        self.MAX_POSITION_LOAD = config['positionLoad']
        self.SYMBOL = config['tickerSymbol']

        self.tradeAlgorithm = TradeAlgorithm(self.__enter_position)
        self.positionLock = Lock()
        self.storage = Storage()
        self.positions = self.storage.open_positions()
        self.tickHistory = priceHistory
        
    
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

        ma = self.tradeAlgorithm.evaluate(self.tickHistory)

        for p in self.positions:
            p.notify_close(tickPrice, ma)

        self.tickHistory = self.tickHistory[-120:]
        
    def __enter_position(self) -> None:
        if len(self.positions) < self.MAX_POSITION_LOAD:
            new_position = Position.create_position(self.tickHistory[-1], self.SYMBOL)
            self.storage.new_position(new_position)
            self.positions.append(new_position)