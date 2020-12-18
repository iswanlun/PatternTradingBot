
This bot requires a config.py file which contains the following paramenters

config = {
    'coinGeckoApi' : CoinGecko api endpoint,
    'coinGeckoHist' : CoinGecko api history endpoint,
    'binanceWSS' : Binance kline stream,
    'binanceSysTime' :  Binace server time api,
    'binanceHist' : Biance history api endpoint,
    'period' : kline period in seconds,
    'tickerSymbol' : Ticker symbol for asset,
    'bBandRange' : Bollinger Band range,
    'bBandWidth' : Bollinger Band multiplier,
    'bBandType' : BBand type,
    'rsiPeriod' : RSI period,
    'maPeriod' : Moving average period,
    'maType' : Moving average type,
    'targetNet' : Target yield for each trade, ex: 5% would be 1.05,
    'spikeNet': Price spike target,
    'sLoss' : Stop loss percentage,
    'positionLoad' : Number of positions algorythm is authorized to hold at any time,
    'apiKey' : Biance account api key,
    'apiSecret' : Binance account secret key
}