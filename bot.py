import pprint, time, requests, calendar
from Config import config
from PositionManager import TickManager
from Timer import RepeatTimer

API = config['api']
INIT = config['init']

class bot:

    def __init__(self) -> None:
        self.tickManager = TickManager(self.trade_history())
        self.timer = RepeatTimer(2)
        self.timer.start(self)
    
    def event(self):
        responce = requests.get(API)
        jsonData = responce.json()
        pprint.pprint(jsonData)

        self.tickManager.next_tick(jsonData)

    def trade_history(self):
        hist = INIT
        hist = hist.replace("X", str(calendar.timegm(time.gmtime()) - 30000))
        hist = hist.replace("Y", str(calendar.timegm(time.gmtime())))
        initData = requests.get(hist).json()
        return [x[1] for x in initData['prices']]

bot = bot()