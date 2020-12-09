import calendar, time
from config import config
'''
Position will control both database and
finance opperators

'''
class Position:

    def __init__(self, entryPoint, symbol, entryTime=None, units=None, exitPoint=None, exitTime=None, inPosition=True) -> None:
        self.goal = config['targetNet'] * self.entryPoint
        self.entryPoint = entryPoint
        self.entryTime = entryTime
        self.symbol = symbol
        self.units = units
        self.exitPoint = exitPoint
        self.exitTime = exitTime
        self.inPosition = inPosition

    @classmethod 
    def create_position(cls, entryPoint, symbol):
        entryTime = calendar.timegm(time.gmtime())
        units = config["investmentSize"] / entryPoint



        return cls(entryPoint=entryPoint, symbol=symbol, entryTime=entryTime, units=units)


        
    def notify(self, tickPrice):
        if tickPrice >= self.goal:
            self.exit(tickPrice)

    def exit(self, exitPoint):
        self.inPosition = False
        self.exitPoint = exitPoint
        self.exitTime = calendar.timegm(time.gmtime())