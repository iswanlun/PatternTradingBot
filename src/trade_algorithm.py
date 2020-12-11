import talib, numpy as np
from config import config

class TradeAlgorithm():

    def __init__(self, enterTarget) -> None:
        self.MA_PERIOD = config['maPeriod']
        self.MA_TYPE = config['maType']
        self.RSI_PERIOD = config['rsiPeriod']
        self.BB_PERIOD = config['bBandRange']
        self.BB_WIDTH = config['bBandWidth']
        self.BB_TYPE = config['bBandType']
        self.PERIOD = config['period']
        self.enterTarget = enterTarget

    def evaluate(self, close : list, positions : list) -> int:
        ma = talib.MA(np.array(close), self.MA_PERIOD, self.MA_TYPE)[-1]
        rsi = talib.RSI(np.array(close), self.RSI_PERIOD)[-1]
        upper, middle, lower = talib.BBANDS(np.array(close), self.BB_PERIOD, self.BB_WIDTH, self.BB_WIDTH, self.BB_TYPE)
        print("RSI {}".format(str(rsi))) # DEBUG
        print("Lower BBand {}".format(str(lower[-1]))) # DEBUG
        print("Moving Average {}".format(str(ma))) # DEBUG

        for p in positions:
            p.notify_close(close[-1], ma)

        if (rsi < 30) & (close[-1] < lower[-1]):
            self.enterTarget()

        return ma