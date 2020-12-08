
import talib
from Config import config
import numpy as np
from Timer import RepeatTimer

class Position:

    def __init__(self, entryPoint) -> None:
        self.inPosition = True
        self.entryPoint = entryPoint
        self.exitPoint = None
        self.goal = config['targetNet'] * self.entryPoint

    def notify(self, tickPrice):
        if tickPrice >= self.goal:
            self.__exit(tickPrice)

    def __exit(self, exitPoint):
        self.inPosition = False
        self.exitPoint = exitPoint  

class TickManager:

    def __init__(self, priceHistory)  -> None:  
        self.RSI_PERIOD = config['rsiPeriod']
        self.BB_PERIOD = config['bBandRange']
        self.BB_WIDTH = config['bBandWidth']
        self.BB_TYPE = config['bBandType']
        self.PERIOD = config['period']
        self.MAX_POSITION_LOAD = config['positionLoad']

        self.positions = []
        self.close = False
        self.tickHistory = priceHistory
        print(self.tickHistory)
        self.timer = RepeatTimer(self.PERIOD) 
        self.timer.start(self)

    def event(self):
        self.close = True
        print("Closing clandle") # DEBUG

    def __update(self, tickPrice):
        self.rsi = talib.RSI(np.array(self.tickHistory), self.RSI_PERIOD)[-1]
        self.upper, self.middle, self.lower = talib.BBANDS(np.array(self.tickHistory), self.BB_PERIOD, self.BB_WIDTH, self.BB_WIDTH, self.BB_TYPE)
        print("RSI " + self.rsi) # DEBUG
        print("Lower BBand " + self.lower[-1]) # DEBUG

        if (self.rsi < 30) & (tickPrice < self.lower[-1]):
            self.__enter_position()
        
    def __enter_position(self, entryPoint) -> None:
        if len(self.positions) < self.MAX_POSITION_LOAD:
            self.positions.append(Position(entryPoint))

    def next_tick(self, jsonData):

        tickPrice = jsonData['ethereum']['usd']

        for x in self.positions:
            if not x.inPosition:
                self.positions.remove(x)
            else:
                x.notify(tickPrice)

        if self.close:
            self.tickHistory.append(tickPrice)
            self.__update(tickPrice)
            self.close = False