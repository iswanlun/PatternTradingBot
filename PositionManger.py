
'''
The purpose of this class is to handle the calculation of positions.
BUY, SELL, HOLD, NONE
'''

from enum import Enum

class Action(Enum):
    BUY = 1
    SELL = 2
    NONE = 3

class Position(Enum):
    IN_POSITION = 1
    NO_POSITION = 2


class TickManger:

    def __init__(self, position=Position.NO_POSITION):
        super().__init__()
        self.position = position
        self.action = Action.NONE

    def get_action(self) -> Action:
        return self.action
    
    def set_position(self, position):
        self.position = position

    def next_tick(jsonData):
        pass