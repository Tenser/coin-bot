import sys
import matplotlib.pyplot as plt
import ccxt
import etc
import numpy as np

code = sys.argv[1]
limit = int(sys.argv[2])

binance = ccxt.binance()
upbit = ccxt.upbit()
arr1 = []
arr2 = []
rate = etc.get_exchange_rate()
#ohlcvs1 = upbit.fetch_ohlcv('XRP/KRW', timeframe='1d')
#ohlcvs2 = binance.fetch_ohlcv('XRP/USDT', timeframe='1d')
ohlcvs1 = upbit.fetch_ohlcv('XRP/KRW', timeframe='1d', limit=limit)
ohlcvs2 = binance.fetch_ohlcv('XRP/USDT', timeframe='1d', limit=limit)
ohlcvs3 = upbit.fetch_ohlcv(code + '/KRW', timeframe='1d', limit=limit)
ohlcvs4 = binance.fetch_ohlcv(code + '/USDT', timeframe='1d', limit=limit)
for i in range(limit):
    arr1.append((ohlcvs1[i][4] / (ohlcvs2[i][4] * rate) - 1) * 100)
    arr2.append((ohlcvs3[i][4] / (ohlcvs4[i][4] * rate) - 1) * 100)

t = np.arange(limit)
narr1 = np.array(arr1)
narr2 = np.array(arr2)

plt.plot(t, narr1, t, narr2, 'r-')
plt.show()