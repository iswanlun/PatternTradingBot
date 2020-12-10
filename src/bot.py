
from tick_manager import TickManager
from coin_gecko_api import CoinGeckoTrader
from binance_stream import BinanceStream

class Bot:

    def __init__(self) -> None:
        self.tradingApi = BinanceStream()
        self.tradManager = TickManager(self.tradingApi.return_history())
        self.tradingApi.add_listener(self.tradManager)
        self.tradingApi.start()
    
Bot()