import ccxt
import time
from datetime import datetime
import etc

class CopyMoney:
    def __init__(self):
        self.upbit = ccxt.upbit({
            'apiKey': 'usSJmCIHV9BoLM6fWVVIDuBPG2GmOX4HdGBr82xK',
            'secret': 'Qef86e7FYVuK3PjkP807DaxMiGKkkaCra7oCs1ub',
            'options': {
                'createMarketBuyOrderRequiresPrice' : False
            }
        })
        self.informs = None
        self.boughts = []

    def update(self, limit, windows):
        informs = dict()
        #print(1)
        for market in self.upbit.load_markets().keys():
            if market[-3:] == 'KRW' and market[:-4] != 'Tokamak Network' and market[:-4] != 'BTC' and market[:-4] != 'ETH':
                time.sleep(self.upbit.rateLimit / 8000)
                candle = self.upbit.fetchOHLCV(market, '1d', limit=windows+1)
                if len(candle) > windows:
                    #print(market)
                    noise_avg = etc.get_noise_avg(candle)
                    target = candle[-1][1] + (candle[-2][2] - candle[-2][3]) * noise_avg
                    time.sleep(self.upbit.rateLimit / 20000)
                    candle2 = self.upbit.fetchOHLCV(market, '1d', limit=6)
                    noise_avg2 = etc.get_noise_avg(candle2)
                    if candle[-1][4] < target:
                        informs[market] = {
                            'target': target,
                            'noise_avg': noise_avg2
                        } 
        self.informs = etc.filtering(informs, limit)
        print(self.informs)

    def buy(self, limit, importance):
        balance = self.upbit.fetch_balance()
        krw_free = balance['KRW']['free'] * importance
        print(krw_free)
        count = 0
        while count < limit:
            now = datetime.time(datetime.now())
            if now.hour == 8 and now.minute > 30:
                break
            for market in self.informs.keys():
                time.sleep(self.upbit.rateLimit / 8000)
                candle = self.upbit.fetch_ticker(market)
                target = self.informs[market]
                #print(market)
                if candle['close'] >= target:
                    self.upbit.create_market_buy_order(market, krw_free / limit)
                    count += 1
                    del self.informs[market]
                    self.boughts.append(market)
                    print(market)
                    break

    def sell(self):
        while True:
            time.sleep(5)
            now = datetime.now()
            now_hour = datetime.time(now).hour
            if now_hour == 9:
                balance = self.upbit.fetch_balance()
                for market in self.boughts:
                    time.sleep(0.5)
                    self.upbit.create_market_sell_order(market, balance[market[:-4]]['free'])
                self.boughts = []
                break
    
    def run(self, filter_limit, buy_limit, windows, importance):
        while True:
            print('update start!')
            self.update(filter_limit, windows)
            print('update finish!')
            print('buy start!')
            self.buy(buy_limit, importance)
            print('buy finish!')
            print('sell start!')
            self.sell()
            print('sell finish!')
            time.sleep(5)

    """
    def get_noise_avg(self, candle):
        windows = len(candle)-1
        noise_sum = 0
        for i in range(windows):
            noise_sum += 1 - abs(candle[i][1]- candle[i][4]) / (candle[i][2]- candle[i][3])
        noise_avg = noise_sum / windows
        return noise_avg

    def get_min_noise(self, informs, limit):
        res = dict()
        for i in range(limit):
            market_min = None
            noise_min = 1e9
            for market in informs.keys():
                noise_avg = informs[market]['noise_avg']
                if noise_avg < noise_min:
                    market_min = market
                    noise_min = noise_avg
            res[market_min] = informs[market_min]['target']
            del informs[market_min]
            #print(noise_min)
        return res
    """
#cm = CopyMoney()
#cm.run(10, 5, 13, 0.1)
    