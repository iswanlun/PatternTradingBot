import json, time, requests, calendar
from threading import Timer
import websocket, pprint
from ticker_api import TickerAPI
from tick_listener import TickListener
from config import config

# https://binance-docs.github.io/apidocs/spot/en/#public-api-definitions

WSS = config['binanceWSS']
HIST = config['coinGeckoHist']

class BinanceStream(TickerAPI):

    def __init__(self) -> None:
        self.listeners = []
        self.ws = None
        self.isClosed = False
        self.closeTimer = Timer(config['period'])
            
    def add_listener(self, listener: TickListener):
        self.listeners.append(listener)
        
    def on_tick(self, raw):
        tickData = json.loads(raw)
        tickPrice = tickData['k']['c']

        if self.isClosed:
            self.isClosed = False
            for l in self.listeners:
                l.close_event(tickPrice)
        else:
            for l in self.listeners:
                l.tick_event(tickPrice)
        
    def on_close(self, tickPrice):
        self.isClosed = True
        
    def error(self, error):
        print("An error {}".format(str(error)))

    def stream_closed(self, msg):
        print("stream closed {}".format(str(msg)))
        self.closeTimer.stop()
        time.sleep(10)
        self.start()

    def return_history(self) -> list:
        hist = HIST.replace("X", str(calendar.timegm(time.gmtime()) - 30000))
        hist = hist.replace("Y", str(calendar.timegm(time.gmtime())))
        histData = requests.get(hist).json()
        return [x[1] for x in histData['prices']][0::5]

    def start(self):
        self.closeTimer.start(target=self.on_close)
        self.ws = websocket.WebSocketApp(WSS,
                on_message=self.on_tick,
                on_error=self.error,
                on_close=self.stream_closed)
        self.ws.run_forever()