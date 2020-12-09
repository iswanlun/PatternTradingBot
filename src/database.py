
from position_manager import Position

class Database:
    def tick_history() -> list:
        raise NotImplementedError

    def close_tick(tickPrice : float):
        raise NotImplementedError

    def open_positions() -> list:
        raise NotImplementedError

    def new_position(position : Position):
        raise NotImplementedError

    def position_history() -> list:
        raise NotImplementedError