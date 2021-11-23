import ccxt
import time
from datetime import datetime
import etc

class StocasticFutureDeal:
    def __init__(self, market, unit, leverage):
        self.upbit = ccxt.binance({
            'apiKey': 'nJtYtDJrAHnn52vW1SeMqUBwaVMc7Hl46wzbE1QAmH45V1w40ZHwXu1JzjUA1wsP',
            'secret': 'Tp03WrIfSQbyrjQHUsaIoGezf9fZs9md59LCcHinmdjd6BXhfpJuL7fj479wuHeD',
            'options': {
                'createMarketBuyOrderRequiresPrice' : False,
                'defaultType' : 'future'
            }
        })
        self.market = market
        self.sign = 0
        self.unit = unit
        self.leverage = leverage
        self.amount = None

    def setting(self, n, m, t):
        candles = self.upbit.fetchOHLCV(self.market, self.unit, limit=n+m+t-2)
        slow_d, slow_k = etc.get_stocastic_slow_d(candles, n, m, t)
        if slow_k > slow_d:
            self.sign = 1
        else:
            self.sign = -1
        print(slow_d, slow_k, candles[-1][4], self.sign)
        
    def wait(self, n, m, t):
        while True:
            time.sleep(1)
            candles = self.upbit.fetchOHLCV(self.market, self.unit, limit=n+m+t-2)
            slow_d, slow_k = etc.get_stocastic_slow_d(candles, n, m, t)
            #print(slow_d, slow_k, candles[-1][4])
            if self.sign == 1:
                if slow_k - slow_d < 1:
                    self.sign = 0
                    print("wait end", slow_d, slow_k, candles[-1][4])
                    break
            elif self.sign == -1:
                if slow_d - slow_k < 1:
                    self.sign = 0
                    print("wait end", slow_d, slow_k, candles[-1][4])
                    break

    def position_in(self, n, m, t, importance, n2):
        while True:
            time.sleep(1)
            candles = self.upbit.fetchOHLCV(self.market, self.unit, limit=n+m+t-2)
            slow_d, slow_k = etc.get_stocastic_slow_d(candles, n, m, t)
            #print(slow_d, slow_k, candles[-1][4])
            if slow_k - slow_d > 3:
                self.sign = 1
                if slow_d < 40 and self.filtering(n2):
                    usdt = self.upbit.fetch_balance()['USDT']['free']
                    amount = usdt / candles[-1][4] * importance * self.leverage
                    self.upbit.create_order(symbol=self.market, side='buy', type="MARKET", amount=amount)
                    self.amount = amount
                    print("long", slow_d, slow_k, candles[-1][4], self.amount)
                    time.sleep(5)
                    return True
                return False
            elif slow_d - slow_k > 3:
                self.sign = -1
                if slow_d > 60 and self.filtering(n2):
                    usdt = self.upbit.fetch_balance()['USDT']['free']
                    amount = usdt / candles[-1][4] * importance * self.leverage
                    self.upbit.create_order(symbol=self.market, side='sell', type="MARKET", amount=amount)
                    self.amount = amount
                    print("short", slow_d, slow_k, candles[-1][4], self.amount)
                    time.sleep(5)
                    return True
                return False

    def position_out(self, n, m, t):
        remain = True
        while True:
            time.sleep(1)
            candles = self.upbit.fetchOHLCV(self.market, self.unit, limit=n+m+t-1)
            slow_d, slow_k = etc.get_stocastic_slow_d(candles[1:], n, m, t)
            slow_d_before, slow_k_before = etc.get_stocastic_slow_d(candles[:-1], n, m, t)
            #print(slow_d, slow_k, candles[-1][4])
            if self.sign == 1:
                """
                if remain and slow_k < slow_k_before:
                    remain = False
                    self.upbit.create_order(symbol=self.market, side='sell', type="MARKET", amount=self.amount)
                    print("long_out", slow_d, slow_k, candles[-1][4], self.amount)
                    time.sleep(5)
                """
                if slow_k - slow_d < -2:
                    if remain:
                        self.upbit.create_order(symbol=self.market, side='sell', type="MARKET", amount=self.amount)
                        print("long_out", slow_d, slow_k, candles[-1][4], self.amount)
                    self.sign = 0
                    time.sleep(5)
                    break
            elif self.sign == -1:
                """
                if remain and slow_k > slow_k_before:
                    remain = False
                    self.upbit.create_order(symbol=self.market, side='buy', type="MARKET", amount=self.amount)    
                    print("short_out", slow_d, slow_k, candles[-1][4], self.amount)
                    time.sleep(5)
                """
                if slow_k - slow_d > 2:
                    if remain:
                        self.upbit.create_order(symbol=self.market, side='buy', type="MARKET", amount=self.amount)
                        print("short_out", slow_d, slow_k, candles[-1][4], self.amount)
                    self.sign = 0
                    time.sleep(5)
                    break
        print("sell end", slow_d, slow_k, candles[-1][4], self.amount)

    def filtering(self, n):
        candles = self.upbit.fetchOHLCV(self.market, self.unit, limit=n*2-1)
        cci = etc.get_cci(candles, n)
        print(cci)
        if self.sign == 1:
            return cci < -100 or 0 < cci < 100
        elif self.sign == -1:
            return cci > 100 or -100 < cci < 0
        
    def run(self, n, m, t, importance, n2):
        self.setting(n, m, t)
        print("wait start")
        self.wait(n, m, t)
        while True:
            res = self.position_in(n, m, t, importance, n2)
            if not res:
                print("wait start")
                self.wait(n, m, t)
                continue
            self.position_out(n, m, t)


class StocasticAndRsi:

    def __init__(self, market, amount):
        self.binance = ccxt.binance({
            'apiKey': 'nJtYtDJrAHnn52vW1SeMqUBwaVMc7Hl46wzbE1QAmH45V1w40ZHwXu1JzjUA1wsP',
            'secret': 'Tp03WrIfSQbyrjQHUsaIoGezf9fZs9md59LCcHinmdjd6BXhfpJuL7fj479wuHeD',
            'options': {
                'createMarketBuyOrderRequiresPrice' : False,
                'defaultType' : 'future'
            }
        })
        self.market = market
        self.amount = amount

    def start(self, unit):
        while True:
            time.sleep(5)
            candles = self.binance.fetchOHLCV(self.market, unit, limit=16)
            slow_k = etc.get_stocastic_slow_k(candles[-7:], 5, 3)
            slow_k_before = etc.get_stocastic_slow_k(candles[-8:-1], 5, 3)
            rsi = etc.get_rsi(candles[1:], 14)
            rsi_before = etc.get_rsi(candles[:-1], 14)
            print(slow_k_before, slow_k, rsi_before, rsi)
            if slow_k > slow_k_before+2 and rsi > rsi_before:
                print("long", candles[-1][4])
                return True
            elif slow_k < slow_k_before-2 and rsi < rsi_before:
                print("short", candles[-1][4])
                return False

    def long(self, unit):
        #self.binance.create_order(symbol=self.market, side='buy', type="MARKET", amount=self.amount)
        while True:
            time.sleep(5)
            candles = self.binance.fetchOHLCV(self.market, unit, limit=16)
            slow_k = etc.get_stocastic_slow_k(candles[-7:], 5, 3)
            slow_k_before = etc.get_stocastic_slow_k(candles[-8:-1], 5, 3)
            rsi = etc.get_rsi(candles[1:], 14)
            rsi_before = etc.get_rsi(candles[:-1], 14)
            if slow_k < slow_k_before-2 and rsi < rsi_before:
                print("short", candles[-1][4])
                break
        #self.binance.create_order(symbol=self.market, side='sell', type="MARKET", amount=self.amount)

    def short(self, unit):
        #self.binance.create_order(symbol=self.market, side='sell', type="MARKET", amount=self.amount)
        while True:
            time.sleep(5)
            candles = self.binance.fetchOHLCV(self.market, unit, limit=16)
            slow_k = etc.get_stocastic_slow_k(candles[-7:], 5, 3)
            slow_k_before = etc.get_stocastic_slow_k(candles[-8:-1], 5, 3)
            rsi = etc.get_rsi(candles[1:], 14)
            rsi_before = etc.get_rsi(candles[:-1], 14)
            if slow_k > slow_k_before+2 and rsi > rsi_before:
                print("long", candles[-1][4])
                break
        #self.binance.create_order(symbol=self.market, side='buy', type="MARKET", amount=self.amount)

    def run(self, unit):
        res = self.start(unit)
        if res:
            while True:
                self.long(unit)
                self.short(unit)
        else:
            while True:
                self.short(unit)
                self.long(unit)
                

