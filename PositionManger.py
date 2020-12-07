
import json, talib

class Position:

    def __init__(self, inPosition=False, entryPoint=None) -> None:
        self.inPosition = inPosition
        self.entryPoint = entryPoint
        self.exitPoint = None

    def exit(self, exitPoint) -> float:
        self.inPosition = False
        self.exitPoint = exitPoint
        return self.exitPoint - self.entryPoint


class TickManager:

    def __init__(self)  -> None:
        self.position = None
    
    def __enter_position(self, entryPoint) -> None:
        self.position = Position(True, entryPoint)

    def __exit_position(self, exitPoint) -> None:
        self.position.exit(exitPoint)

    def next_tick(jsonData: object) -> str:
        
        
        

        return "?"
