import websocket, json, pprint, talib, time
import numpy as np
from datetime import datetime
from display_graphs import RSIGraph, BBandGraph
from Database import Database

'''
Binance streams are disconnected every 24hrs
'''
SOCKET = 'wss://stream.binance.com:9443/ws/ethusdt@kline_1m'

#FORMAT DATA
BBAND_RANGE = 28
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'

ticks = []
tick_times = []
start_time = int(round(time.time() * 1000))
g_out = RSIGraph(RSI_OVERSOLD, RSI_OVERBOUGHT)
bands_graph = BBandGraph()

trades_database = Database()

def on_open(ws):
    print('Connection is established.')
    print(start_time)

def on_close(ws):
    print('Connection terminated')

def on_message(ws, message):
    global ticks, tick_times, g_out
    
    json_data = json.loads(message)
    pprint.pprint(json_data)

    candle = json_data['k']
    candle_close = candle['x']

    ticks.append(float(candle['c']))
    tick_times.append(int(json_data['E']) - start_time)
    
    print(ticks)
    
    if len(ticks) == 50:
        ticks.pop(0)
        tick_times.pop(0)

    if len(ticks) > BBAND_RANGE:
        upper, mid, lower = talib.BBANDS(np.array(ticks, dtype=float), timeperiod=BBAND_RANGE, nbdevup=2, nbdevdn=2, matype=0)
        upper = upper[np.isfinite(upper)]
        lower = lower[np.isfinite(lower)]
        print(upper)
        print(lower)
        if len(tick_times) != len(upper):
            t = len(tick_times) - len(upper)
            short_tick_times = tick_times[t:]
            short_ticks = ticks[t:]
        bands_graph.update(upper, lower, short_tick_times, short_ticks)

    if len(ticks) > RSI_PERIOD:
        np_ticks_array = np.array(ticks)
        rsi = talib.RSI(np_ticks_array, RSI_PERIOD) # array to use for matplotlib
        rsi = rsi[np.isfinite(rsi)]
        if len(rsi) != len(tick_times):
            t = len(tick_times) - len(rsi)
            short_tick_times = tick_times[t:]
        print(tick_times) ###
        print(rsi) ###
        g_out.update(short_tick_times, rsi)


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
arr = trades_database.load_current_positions(TRADE_SYMBOL)
print(arr)
ws.run_forever()