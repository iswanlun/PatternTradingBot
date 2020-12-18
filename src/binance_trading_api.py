import pprint
from broker import Broker
from binance.client import Client
from binance.enums import *
from config import config

# ref : https://python-binance.readthedocs.io/en/latest/account.html

class Binance(Broker):

    def __init__(self) -> None:
       self.client = Client(config['apiKey'], config['apiSecret'])
       self.quanity = config['tradeSize']

    def purchase_shares(self, symbol):
        order = self.client.order_market_buy(
            symbol=symbol,
            quantity=self.quanity
        )
        pprint.pprint(order)

    def sell_shares(self, symbol):
        order = self.client.order_market_sell(
            symbol=symbol,
            quantity=self.quanity
        )
        pprint.pprint(order)

    def test_order(self, symbol):
        order = self.client.create_test_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=100,
            price='0.00001'
        )
        pprint.pprint(order)