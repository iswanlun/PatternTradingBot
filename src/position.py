import calendar, time
from config import config

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

    @classmethod 
    def create_position(cls, entryPoint, symbol):
        entryTime = calendar.timegm(time.gmtime())
        print("position created, price {}, time {}".format(str(entryPoint), str(entryTime))) # DEBUG - Swap for broker interaction
        return cls(entryPoint=entryPoint, symbol=symbol, entryTime=entryTime)

    def notify(self, tickPrice, onClose):
        if tickPrice >= self.spike:
            self.exit(tickPrice)
        elif onClose & (tickPrice >= self.goal):
            self.exit(tickPrice)

    def exit(self, exitPoint):
        self.inPosition = False
        self.exitPoint = exitPoint
        self.exitTime = calendar.timegm(time.gmtime())