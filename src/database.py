
from position_manager import Position

class Database:
    def open_positions() -> list:
        raise NotImplementedError

    def new_position(position : Position):
        raise NotImplementedError

    def close_position(position : Position):
        raise NotImplementedError

    def position_history() -> list:
        raise NotImplementedError