from config import config

class Position:


    def __init__(self, entryPoint, symbol, units) -> None:
        self.entryPoint = entryPoint
        self.goal = config['targetNet'] * self.entryPoint
        self.symbol = symbol
        self.units = units
        self.inPosition = True
        

    def notify(self, tickPrice):
        if tickPrice >= self.goal:
            self.exit(tickPrice)

    def exit(self, exitPoint):
        self.inPosition = False
        self.exitPoint = exitPoint

