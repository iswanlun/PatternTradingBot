import websocket, json, pprint, talib, time
import numpy as np
from datetime import datetime
from display_graphs import RSIGraph



#RSI DATA
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

g_out = RSIGraph(RSI_OVERSOLD, RSI_OVERBOUGHT)

def show():
    time.sleep(2)
    g_out.update([1,2,3,4,5], [20,20,40,50,30])
    time.sleep(0.5)
    g_out.update([7,8,9,10,11], [20,10,10,40,30])
    time.sleep(0.5)
    g_out.update([3,4,5,6,7], [20,30,40,20,10])
    time.sleep(0.5)
    g_out.update([1,2,3,4,5], [20,20,40,50,30])
    time.sleep(0.5)
    g_out.update([7,8,9,10,11], [20,10,10,40,30])
    time.sleep(0.5)
    g_out.update([3,4,5,6,7], [20,30,40,20,10])
    time.sleep(0.5)

def bands():
    closes = [381.39, 381.4, 381.4, 381.39, 381.38, 381.41, 
    381.41, 381.4, 381.4, 381.4, 381.41, 381.41, 381.4, 381.39, 
    381.4, 381.4, 381.4, 381.39, 381.39, 381.4, 381.4, 381.39, 381.4]
    upper, mid, lower = talib.BBANDS(np.array(closes, dtype=float), timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    print(upper)
    print(lower)
    print(mid)
bands()