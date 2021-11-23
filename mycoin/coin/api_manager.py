import ccxt
import pyupbit
import kakao_api
import etc
from coin import Coin
import time

class ApiManager:
    def __init__(self, simbols = ["XRP", "TRX", "EOS"], kp=1.03, rp=0.97):
        self.coins = []
        self.binance = ccxt.binance({
            'apiKey': 'nJtYtDJrAHnn52vW1SeMqUBwaVMc7Hl46wzbE1QAmH45V1w40ZHwXu1JzjUA1wsP',
            'secret': 'Tp03WrIfSQbyrjQHUsaIoGezf9fZs9md59LCcHinmdjd6BXhfpJuL7fj479wuHeD',
            'options': {
                'createMarketBuyOrderRequiresPrice' : False
            }
        })
        self.upbit = ccxt.upbit({
            'apiKey': 'usSJmCIHV9BoLM6fWVVIDuBPG2GmOX4HdGBr82xK',
            'secret': 'Qef86e7FYVuK3PjkP807DaxMiGKkkaCra7oCs1ub',
            'options': {
                'createMarketBuyOrderRequiresPrice' : False
            }
        })
        self.pu = pyupbit.PyUpbit()
        #self.ka = kakao_api.KakaoApi()
        #self.exchange_rate = etc.get_exchange_rate()
        self.exchange_rate = None
        self.update_exchange_rate()
        print(self.exchange_rate)
        for simbol in simbols:
            coin = Coin(simbol, self.pu.get_current_price("KRW-" + simbol), self.binance.fetch_ticker(simbol + '/USDT')['close'] * self.exchange_rate, kp, rp)
            self.coins.append(coin)
            rate = (coin.rate - 1) * 100
            #print(coin.upbit_price, coin.binance_price)
            print(coin.rate)
            if coin.sign == 1:
                #self.ka.msg_send({"title": "김치 프리미엄", "market": coin.market, "rate": rate})
                print("김치 프리미엄")
            elif coin.sign == -1:
                #self.ka.msg_send({"title": "역 프리미엄", "market": coin.market, "rate": rate})
                print("역 프리미엄")
            else:
                #self.ka.msg_send({"title": "No", "market": coin.market, "rate": rate})
                print("NO")
        #print(self.coins[0].sign)

    def update(self):
        for coin in self.coins:
            simbol = coin.market
            before_sign = coin.sign
            coin.update(self.pu.get_current_price("KRW-" + simbol), self.binance.fetch_ticker(simbol + '/USDT')['close'] * self.exchange_rate)
            after_sign = coin.sign
            rate = (coin.rate - 1) * 100
            print(coin.rate)
            if after_sign == 1:
                if before_sign != 1:
                    #self.ka.msg_send({"title": "김치 프리미엄", "market": coin.market, "rate": rate})
                    print("김치 프리미엄")
            elif after_sign == -1:
                if before_sign != -1:
                    #self.ka.msg_send({"title": "역 프리미엄", "market": coin.market, "rate": rate})
                    print("역 프리미엄")
            else:
                if before_sign == 1:
                    #self.ka.msg_send({"title": "김치 프리미엄 해제", "market": coin.market, "rate": rate})
                    print("NO")
                if before_sign == -1:
                    #self.ka.msg_send({"title": "역 프리미엄 해제", "market": coin.market, "rate": rate})
                    print("NO")

    def search_min_rate(self, standard):
        min_rate = 1e9
        min_market = None
        for coin in self.coins:
            if coin.rate < min(standard, min_rate):
                min_rate = coin.rate
                min_market = coin.market
        return min_market

    def upbit_buy_and_withdraw(self, code):
        balance = self.upbit.fetch_balance()
        funding_fee = self.pu.get_funding_fee(code)
        address = self.binance.fetchDepositAddress(code)

        print(balance['KRW']['free'] * 0.99)
        print(self.upbit.create_market_buy_order(code + '/KRW', balance['KRW']['free'] * 0.995))
        time.sleep(5)

        balance = self.upbit.fetch_balance()
        print(balance[code]['free'])
        max_balance = int((balance[code]['free'] - funding_fee) * 1e5) / 1e5
        print(max_balance)
        #print(binance.fetch_funding_fees()['withdraw']['XRP'])
        print(self.upbit.withdraw(code, max_balance, address['address'], tag=address['tag']))

        return max_balance

    def binance_sell(self, code):
        while True:
            time.sleep(3)
            withdrawals = self.upbit.fetch_withdrawals(code)
            deposits = self.binance.fetch_deposits(code)
            if withdrawals and deposits and withdrawals[-1]['txid'] == deposits[-1]['txid']:
                time.sleep(30)
                balance = self.binance.fetch_balance()
                print(balance[code]['free'])
                print(self.binance.create_market_sell_order(code + '/USDT', balance[code]['free']))
                break

    def update_exchange_rate(self):
        #self.ka.token_rewel()
        self.exchange_rate = etc.get_exchange_rate()

    def run(self, standard):
        i = 0
        while True:
            code = self.search_min_rate(standard)
            if code != None:
                self.upbit_buy_and_withdraw(code)
                self.binance_sell(code)
                break
            
            time.sleep(5)
            i += 1
            if i>10:
                self.update_exchange_rate()
                i = 0

            self.update()
            
        
            
        

            