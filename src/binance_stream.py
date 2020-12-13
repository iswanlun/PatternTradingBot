import json, time, requests, calendar
from timer import RepeatTimer
import websocket, pprint
from ticker_api import TickerAPI
from tick_listener import TickListener
from config import config

# https://binance-docs.github.io/apidocs/spot/en/#public-api-definitions

WSS = config['binanceWSS']
TIME = config['binanceSysTime']
HIST = config['binanceHist']

class BinanceStream(TickerAPI):

    def __init__(self) -> None:
        self.listener = None
        self.ws = None
        self.isClosed = False
        self.closeTimer = RepeatTimer(config['period'])
            
    def add_listener(self, listener: TickListener):
        self.listener = listener
        
    def on_tick(self, raw):
        tickPrice = json.loads(raw)['k']['c']

        self.listener.tick_event(float(tickPrice), self.isClosed)
        self.isClosed = False
        print("Last tick {}".format(tickPrice)) # DEBUG 
        
    def on_close(self):
        self.isClosed = True
        
    def error(self, error):
        print("An error {}".format(str(error)))

    def stream_closed(self, msg):
        print("stream closed {}".format(str(msg)))
        self.closeTimer.stop()
        time.sleep(10)
        self.start()

    def return_history(self) -> list:
        sysTime = requests.get(TIME).json()
        endTime = sysTime['serverTime'] 
        startTime = endTime - (config['period'] * 120000) # last 120 period intervals
        hist = HIST.replace("X", str(startTime))
        hist = hist.replace("Y", str(endTime))
        histData = requests.get(hist).json()
        histValues = []
        for n in histData:
            histValues.append(float(n[1]))
        return histValues

    def start(self):
        self.closeTimer.start(target=self.on_close)
        self.ws = websocket.WebSocketApp(WSS,
                on_message=self.on_tick,
                on_error=self.error,
                on_close=self.stream_closed)
        self.ws.run_forever()