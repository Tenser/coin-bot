import ccxt
import time
from datetime import datetime
from functions.deal import get_candles
import functions.etc as etc

class StocasticFuture:
    def __init__(self, binance, market, unit, n, m, t, gap):
        self.binance = binance
        self.market = market
        self.unit = unit
        self.n = n
        self.m = m
        self.t = t
        self.gap = gap
        self.state = 0
        self.purchase_price = None
    
    def position_in(self):
        flag = False
        candles = get_candles(self.binance, self.market, self.unit, self.n+self.m+self.t-2)
        #candles = self.binance.fetchOHLCV(self.market, self.unit, limit=self.n+self.m+self.t-2)
        slow_d, slow_k = etc.get_stocastic_slow_d(candles, self.n, self.m, self.t)
        if slow_k > slow_d:
            flag = True
        print(flag, slow_k, slow_d)
        while True:
            time.sleep(3)
            candles = get_candles(self.binance, self.market, self.unit, self.n+self.m+self.t-2)
            #candles = self.binance.fetchOHLCV(self.market, self.unit, limit=self.n+self.m+self.t-2)
            slow_d, slow_k = etc.get_stocastic_slow_d(candles, self.n, self.m, self.t)
            if flag and slow_k < slow_d - self.gap:
                if slow_d > 60:
                    self.state = -1
                    self.purchase_price = candles[-1][4]
                    return 'short', candles[-1][4]
                else:
                    flag = False
                print(flag, slow_k, slow_d)
            elif not flag and slow_k > slow_d + self.gap:
                if slow_d < 40:
                    self.state = 1
                    self.purchase_price = candles[-1][4]
                    return 'long', candles[-1][4]
                else:
                    flag = True
                print(flag, slow_k, slow_d)

    def position_out(self):
        while True:
            time.sleep(3)
            candles = get_candles(self.binance, self.market, self.unit, 1)
            #candles = self.binance.fetchOHLCV(self.market, self.unit, limit=1)
            current_price = candles[0][4]
            if self.state == -1:
                if current_price <= self.purchase_price * 0.991:
                    self.state = 0
                    self.purchase_price = None
                    return 'short_out', 'win'
                elif current_price >= self.purchase_price * 1.011:
                    self.state = 0
                    self.purchase_price = None
                    return 'short_out', 'lose'
            elif self.state == 1:
                if current_price >= self.purchase_price * 1.011:
                    self.state = 0
                    self.purchase_price = None
                    return 'long_out', 'win'
                elif current_price <= self.purchase_price * 0.991:
                    self.state = 0
                    self.purchase_price = None
                    return 'long_out', 'lose'