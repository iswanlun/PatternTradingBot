
from tick_manager import TickManager
from coin_gecko import CoinGeckoTrader

class Bot:

    def __init__(self) -> None:
        self.tradeingApi = CoinGeckoTrader()
        self.tradeManager = TickManager(self.tradeingApi.return_history())
        self.tradeingApi.add_listener(self.tradeManager)
        self.tradeingApi.start()
    
Bot()