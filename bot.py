import websocket, json, pprint, talib, time
import numpy as np
from datetime import datetime
from PositionManger import Action, Position, TickManger


SOCKET = 'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'

class bot:

    def __init__(self) -> None:
        super().__init__()
        self.tickManger = TickManger(Position.NONE)
        self.ws = websocket.WebSocketApp(SOCKET, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)

    def on_open(ws):
        print('Connection is established.')

    def on_close(ws):
        print('Connection terminated')
    
    def run(self):
        self.ws.run_forever()

    def on_message(self, ws, message):

        jsonData = json.loads(message)
        pprint.pprint(jsonData)

        self.tickManger(jsonData)



bot = bot()
bot.run()
