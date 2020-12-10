
import time, requests, calendar, pprint
from tick_listener import TickListener
from ticker_api import TickerAPI
from timer import RepeatTimer
from config import config

API = config['coinGeckoApi']
HIST = config['coinGeckoHist']

class CoinGeckoTrader(TickerAPI):

    def __init__(self) -> None:
        self.listeners = []
        self.tickTimer = RepeatTimer(2)
        self.closeTimer = RepeatTimer(config['period'])
        
    def add_listener(self, listener : TickListener):
        self.listeners.append(listener)
    
    def start(self):
        self.tickTimer.start(self.on_tick)
        self.closeTimer.start(self.on_close)

    def on_tick(self):
        jsonData = requests.get(API).json()
        tickPrice = jsonData['ethereum']['usd']

        for l in self.listeners:
            l.tick_event(tickPrice, False)

        pprint.pprint(jsonData) # DEBUG

    def on_close(self):
        jsonData = requests.get(API).json()
        closePrice = jsonData['ethereum']['usd']

        for l in self.listeners:
            l.tick_event(closePrice, True)

        pprint.pprint(jsonData) # DEBUG

    def return_history(self) -> list:
        hist = HIST.replace("X", str(calendar.timegm(time.gmtime()) - 30000))
        hist = hist.replace("Y", str(calendar.timegm(time.gmtime())))
        histData = requests.get(hist).json()
        return [x[1] for x in histData['prices']][0::5]