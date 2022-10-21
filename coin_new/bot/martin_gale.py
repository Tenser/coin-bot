import ccxt
import time
from datetime import datetime
import functions.deal as deal
from helper.stocastic import StocasticFuture

class MartinGaleBot:
    def __init__(self, market, unit, n, m, t, gap):
        self.binance = ccxt.binance({
            'apiKey': 'nJtYtDJrAHnn52vW1SeMqUBwaVMc7Hl46wzbE1QAmH45V1w40ZHwXu1JzjUA1wsP',
            'secret': 'Tp03WrIfSQbyrjQHUsaIoGezf9fZs9md59LCcHinmdjd6BXhfpJuL7fj479wuHeD',
            'options': {
                'createMarketBuyOrderRequiresPrice' : False,
                'defaultType' : 'future'
            }
        })
        self.market = market
        self.deal_helper = StocasticFuture(self.binance, market, unit, n, m, t, gap)
        #self.asset = 10
        usdt = deal.get_usdt(self.binance)
        self.start = usdt / 250
        self.count = 0

        print(usdt, self.start)
        
    def run(self):
        while True:
            bet = self.start * (2 ** self.count) 

            print("position_in start")
            position, purchase_price = self.deal_helper.position_in()
            amount = (bet / purchase_price) * 100
            print("{}포지션 진입, 매수가격: {}, 배팅금액: {}, amount: {}".format(position, purchase_price, bet, amount))
            #return
            if position == 'long':
                deal.long_in(self.binance, self.market, amount)
                #self.binance.create_order(symbol=self.market+'/USDT', side='sell', type="MARKET", amount=amount, params={'positionSide': position})
            else:
                deal.short_in(self.binance, self.market, amount)
                #self.binance.create_order(symbol=self.market+'/USDT', side='buy', type="MARKET", amount=amount, params={'positionSide': position})

            print("position_out start")
            position_out, result = self.deal_helper.position_out()
            if position == 'long':
                deal.long_out(self.binance, self.market, amount)
                #self.binance.create_order(symbol=self.market+'/USDT', side='sell', type="MARKET", amount=amount, params={'positionSide': position})
            else:
                deal.short_out(self.binance, self.market, amount)
                #self.binance.create_order(symbol=self.market+'/USDT', side='buy', type="MARKET", amount=amount, params={'positionSide': position})
            if result == 'win':
                #self.asset += bet
                self.count = 0
                self.start = deal.get_usdt(self.binance) / 200
            else:
                #self.asset -= bet
                self.count += 1
            
            print(position_out, result, '남은 금액:', deal.get_usdt(self.binance))
            #print(position_out, result, '남은 금액:', self.asset)