
import talib, Config
import numpy as np
from Timer import RepeatTimer

class Position:

    def __init__(self, entryPoint) -> None:
        self.inPosition = True
        self.entryPoint = entryPoint
        self.exitPoint = None
        self.goal = Config.config['targetNet'] * self.entryPoint

    def exit(self, exitPoint) -> float:
        self.inPosition = False
        self.exitPoint = exitPoint
        return self.exitPoint - self.entryPoint


class TickManager:

    def __init__(self, priceHistory)  -> None:
        self.position = None
        self.tickHistory = priceHistory
        self.timer = RepeatTimer(5)
        self.timer.start(self)
        self.close = False
        print(self.tickHistory) # DEBUG

    def event(self):
        self.close = True
        print("Closing clandle") # DEBUG

    def __update(self):
        self.movingAverage = talib.MA(np.array(self.tickHistory), timeperiod=25, matype=0)[-1]
        self.rsi = talib.RSI(np.array(self.tickHistory), timeperiod=18)[-1]
        print(self.movingAverage) # DEBUG
        print(self.rsi) # DEBUG
    
    def __enter_position(self, entryPoint) -> None:
        self.position = Position(entryPoint)

    def __exit_position(self, exitPoint) -> None:
        self.position.exit(exitPoint)

    def next_tick(self, jsonData):

        tickPrice = jsonData['ethereum']['usd']

        if self.position:
            if self.position.inPosition & tickPrice >= self.position.goal:
                self.__exit_position(tickPrice)

        if self.close:
            self.tickHistory.append(tickPrice)
            self.__update()
            self.close = False
        

