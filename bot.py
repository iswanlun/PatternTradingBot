import websocket, json, pprint, time
from Config import config
from PositionManger import TickManager

SOCKET = config.get('socket')

class bot:

    def __init__(self) -> None:
        self.tickManger = TickManager()

    def on_open(self, ws):
        print('Connection is established.')

    def on_close(self, ws):
        print('Connection terminated')
        time.sleep(10)
        self.run()
    
    def run(self):
        self.ws = websocket.WebSocketApp(SOCKET, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)
        self.ws.run_forever()

    def on_message(self, ws, message):

        jsonData = json.loads(message)
        pprint.pprint(jsonData)

        self.tickManger(jsonData)


bot = bot()
bot.run()
