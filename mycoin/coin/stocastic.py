import ccxt
import time
from datetime import datetime
import etc

class StocasticDeal:
    def __init__(self, market):
        self.upbit = ccxt.upbit({
            'apiKey': 'usSJmCIHV9BoLM6fWVVIDuBPG2GmOX4HdGBr82xK',
            'secret': 'Qef86e7FYVuK3PjkP807DaxMiGKkkaCra7oCs1ub',
            'options': {
                'createMarketBuyOrderRequiresPrice' : False
            }
        })
        self.market = market
        self.sign = 1
        
    def wait(self, n, m, t, unit):
        while True:
            time.sleep(1.5)
            candles = self.upbit.fetchOHLCV(self.market, unit, limit=n+m+t-2)
            slow_d, slow_k = etc.get_stocastic_slow_d(candles, n, m, t)
            #print(slow_d, slow_k, candles[-1][4])
            if slow_d - slow_k > -1:
                #self.upbit.create_market_sell_order(market, balance)
                print("wait end", slow_d, slow_k, candles[-1][4])
                break

    def buy(self, n, m, t, importance, unit, gap):
        while True:
            time.sleep(1.5)
            candles = self.upbit.fetchOHLCV(self.market, unit, limit=n+m+t-2)
            slow_d, slow_k = etc.get_stocastic_slow_d(candles, n, m, t)
            #print(slow_d, slow_k, candles[-1][4])
            if slow_k - slow_d > gap:
                if slow_d < 60:
                    balance = self.upbit.fetch_balance()
                    krw_free = balance['KRW']['free'] * importance
                    self.upbit.create_market_buy_order(self.market, krw_free)
                    print("buy", slow_d, slow_k, candles[-1][4])
                    time.sleep(5)
                    return True
                return False

    def sell(self, n, m, t, unit):
        while True:
            time.sleep(1.5)
            candles = self.upbit.fetchOHLCV(self.market, unit, limit=n+m+t-2)
            slow_d, slow_k = etc.get_stocastic_slow_d(candles, n, m, t)
            #print(slow_d, slow_k, candles[-1][4])
            if slow_d - slow_k > 0:
                balance = self.upbit.fetch_balance()
                if self.market[:-4] in balance:
                    self.upbit.create_market_sell_order(self.market, balance[self.market[:-4]]['free'])
                    print("sell", slow_d, slow_k, candles[-1][4])
                    time.sleep(5)
                break
        
    def run(self, n, m, t, importance, unit, gap):
        
        while True:
            print("wait start")
            self.wait(n, m, t, unit)
            balance = self.upbit.fetch_balance()
            krw_free = balance['KRW']['free'] * importance
            print(krw_free)
            res = self.buy(n, m, t, importance, unit, gap)
            if not res:
                continue
            self.sell(n, m, t, unit)
            #self.sell(n, m, t, 0, unit)

#sd = StocasticDeal('DOGE/KRW')
#sd.run(5, 3, 3, 0.5, '1h', 3)


        