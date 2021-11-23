import ccxt
import time
from datetime import datetime
import etc

class CopyMoney2:
    def __init__(self):
        self.upbit = ccxt.upbit({
            'apiKey': 'usSJmCIHV9BoLM6fWVVIDuBPG2GmOX4HdGBr82xK',
            'secret': 'Qef86e7FYVuK3PjkP807DaxMiGKkkaCra7oCs1ub',
            'options': {
                'createMarketBuyOrderRequiresPrice' : False
            }
        })
        self.informs = None
        self.boughts = dict()
        

    def run(self, filter_limit, buy_limit, windows, importance):
        time.sleep(3)
        print('update informs start!')
        self.update_target(filter_limit, windows)
        print('update informs finish!')
        balance = self.upbit.fetch_balance()
        krw_free = balance['KRW']['free'] * importance
        volume = krw_free / buy_limit
        print(volume)
        count = 0

        is_update_target = True
        is_update_sell_target = True

        while True:
            now = datetime.time(datetime.now())

            if not is_update_sell_target and now.minute < 5:
                time.sleep(5)
                print('update boughts start!')
                self.update_sell_target()
                print('update boughts finish!')
                is_update_sell_target = True
                print('is_update_sell_target', is_update_sell_target)
                if not is_update_target and now.hour == 11:
                    print('update informs start!')
                    self.update_target(filter_limit, windows)
                    print('update informs finish!')
                    is_update_target = True
                    print('is_update_target', is_update_target)

            if is_update_sell_target and now.minute > 5:
                is_update_sell_target = False
                print('is_update_sell_target', is_update_sell_target)
                if is_update_target:
                    is_update_target = False
                    print('is_update_target', is_update_target)

            if not 9 <= now.hour < 11:
                for market in self.informs.keys():
                    time.sleep(self.upbit.rateLimit / 8000)
                    #print(market)
                    buy_sign = count < buy_limit
                    res = self.buy(market, volume, buy_sign=buy_sign)
                    if res == 1: 
                        count += 1
                        print(count)
                        break
                    elif res == -1:
                        print(count)
                        break


            for market in self.boughts.keys():
                time.sleep(self.upbit.rateLimit / 8000)
                #print(market)
                if self.sell(market):
                    count -= 1
                    print(count)
                    break

    def update_target(self, limit, windows):
        informs = dict()
        for market in self.upbit.load_markets().keys():
            if market[-3:] == 'KRW' and market[:-4] != 'Tokamak Network' and market[:-4] != 'BTC' and market[:-4] != 'ETH' and market[:-4] != 'BTT':
                time.sleep(self.upbit.rateLimit / 12000)
                target = self.get_target(market, '1d', windows+1)
                #print(target)
                if target != -1:          
                    time.sleep(self.upbit.rateLimit / 12000)
                    candle2 = self.upbit.fetchOHLCV(market, '1d', limit=6)
                    noise_avg2 = etc.get_noise_avg(candle2)
                    
                    if candle2[-1][4] < target:
                        #print(candle2[-1], target)
                        informs[market] = {
                            'target': target,
                            'noise_avg': noise_avg2
                        } 
        print(len(informs))
        self.informs = etc.filtering(informs, limit)
        print(self.informs)

    def update_sell_target(self):
        for market in self.boughts.keys():
            self.boughts[market] = self.get_target(market, '1h', 25, sell=True)
            print(self.boughts)

    def buy(self, market, volume, buy_sign=True):
        candle = self.upbit.fetch_ticker(market)
        target = self.informs[market]
        #print(market)
        if candle['close'] >= target:
            del self.informs[market]
            if buy_sign:
                self.upbit.create_market_buy_order(market, volume)
                self.boughts[market] = self.get_target(market, '1h', 25, sell=True)
                print("buy", market, self.boughts)
                return 1
            else:
                print("delete", market, self.boughts, self.informs)
                return -1
        return 0

    def sell(self, market):
        candle = self.upbit.fetch_ticker(market)
        target = self.boughts[market]
        if candle['close'] < target:
            balance = self.upbit.fetch_balance()
            self.upbit.create_market_sell_order(market, balance[market[:-4]]['free'])
            del self.boughts[market]
            print("sell", market, self.boughts)
            return True
        return False

    def get_target(self, market, unit, limit, sell=False):
        #print(market, limit)
        candle = self.upbit.fetchOHLCV(market, unit, limit=limit)
        #print(candle)
        if len(candle) < limit:
            print(market, -1)
            return -1

        noise_avg = etc.get_noise_avg(candle)
        if sell:
            target = candle[-1][1] - (candle[-2][2] - candle[-2][3]) * noise_avg
        else:
            target = candle[-1][1] + (candle[-2][2] - candle[-2][3]) * noise_avg
        return target

    
    