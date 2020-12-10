import json, time, requests, calendar
import websocket, pprint
from ticker_api import TickerAPI
from tick_listener import TickListener
from config import config

WSS = config['binanceWSS']
HIST = config['coinGeckoHist']

class BinanceStream(TickerAPI):

    def __init__(self) -> None:
        self.listeners = []
        self.ws = None
            

    def add_listener(self, listener: TickListener):
        self.listeners.append(listener)
        
    def on_tick(self, raw):
        tickData = json.loads(raw)
        candle = tickData['k']
        tickPrice = candle['c']

        if candle['x']:
            self.on_close(tickPrice)
        else:
            for l in self.listeners:
                l.tick_event(tickPrice)
        
        pprint.pprint(tickData) # DEBUG
        
    def on_close(self, tickPrice):
        
        for l in self.listeners:
            l.close_event(tickPrice)

    def error(self, error):
        print("An error {}".format(str(error)))

    def stream_closed(self, msg):
        print("stream closed {}".format(str(msg)))
        time.sleep(10)
        self.start()

    def return_history(self) -> list:
        hist = HIST.replace("X", str(calendar.timegm(time.gmtime()) - 30000))
        hist = hist.replace("Y", str(calendar.timegm(time.gmtime())))
        histData = requests.get(hist).json()
        return [x[1] for x in histData['prices']][0::5]

    def start(self):
        self.ws = websocket.WebSocketApp(WSS,
                on_message=self.on_tick,
                on_error=self.error,
                on_close=self.stream_closed)
        self.ws.run_forever()