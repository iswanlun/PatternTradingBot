import unittest, os, sys
sys.path.append(os.getcwd() + "\\src")

from binance_stream import BinanceStream
import talib
import numpy as np

class BinanceStreamTests(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.stream = BinanceStream()

    def test_history(self):
        hist = self.stream.return_history()
        print(hist)
        self.assertEqual(len(hist), 200)

    def test_analysis(self):
        hist = self.stream.return_history()
        upper, middle, lower = talib.BBANDS(np.array(hist), 99, 2, 2, 0)
        margin = upper - lower
        print(margin)
        self.assertEqual(len(margin), len(hist))

unittest.main()