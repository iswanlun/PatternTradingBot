import json
from src.tick_listener import TickListener

class TickerAPI:

    def add_listener(self, listener : TickListener):
        raise NotImplementedError

    def on_tick(tickPrice : json):
        raise NotImplementedError

    def on_close():
        raise NotImplementedError

    def return_history():
        raise NotImplementedError

    def start():
        raise NotImplementedError