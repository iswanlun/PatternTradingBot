import json, pprint, time, requests
from Config import config
from PositionManger import TickManager
from Timer import RepeatTimer

API = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'

class bot:

    def __init__(self) -> None:
        self.tickManager = TickManager()
        self.timer = RepeatTimer(2)
        self.timer.start(self)
    
    def event(self):
        responce = requests.get(API)
        jsonData = responce.json()
        pprint.pprint(jsonData)

        self.tickManager.next_tick(jsonData)

bot = bot()

