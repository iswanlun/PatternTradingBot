import calendar, time
from config import config
from binance_trading_api import Binance

class Position:

    def __init__(self, entryPoint, symbol, entryTime=None, units=None, exitPoint=None, exitTime=None) -> None:
        self.spike = config['spikeNet'] * entryPoint
        self.goal = config['targetNet'] * entryPoint
        self.entryPoint = entryPoint
        self.entryTime = entryTime
        self.symbol = symbol
        self.units = units
        self.exitPoint = exitPoint
        self.exitTime = exitTime
        self.inPosition = True
        self.broker = Binance()
        self.broker.purchase_shares(self.symbol)

    @classmethod 
    def create_position(self, cls, entryPoint, symbol):
        entryTime = calendar.timegm(time.gmtime())
        print("position created, price {}, time {}".format(str(entryPoint), str(entryTime))) # DEBUG
        return cls(entryPoint=entryPoint, symbol=symbol, entryTime=entryTime)

    def notify(self, tickPrice):
        if tickPrice >= self.spike:
            self.exit(tickPrice)

    def notify_close(self, tickPrice, movingAverage):
        if (tickPrice >= movingAverage) & (tickPrice >= self.goal):
            self.exit(tickPrice)

    def exit(self, exitPoint):
        self.broker.sell_shares(self.symbol)
        self.inPosition = False
        self.exitPoint = exitPoint
        self.exitTime = calendar.timegm(time.gmtime())