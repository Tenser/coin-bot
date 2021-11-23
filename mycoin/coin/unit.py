import ccxt
import time
from datetime import datetime
#import etc

class DualPositionUnit:

    def __init__(self, info, usdt, importance, leverage):
        self.binance = ccxt.binance({
            'apiKey': 'nJtYtDJrAHnn52vW1SeMqUBwaVMc7Hl46wzbE1QAmH45V1w40ZHwXu1JzjUA1wsP',
            'secret': 'Tp03WrIfSQbyrjQHUsaIoGezf9fZs9md59LCcHinmdjd6BXhfpJuL7fj479wuHeD',
            'options': {
                'createMarketBuyOrderRequiresPrice' : False,
                'defaultType' : 'future',
            }
        })
        self.symbol = info['symbol']
        self.standard_init_long = info['additionLong']
        self.standard_long = info['standardLong']
        self.addition_long = info['additionLong']
        self.standard_init_short = info['additionShort']
        self.standard_short = info['standardShort']
        self.addition_short = info['additionShort']
        price = self.binance.fetch_ticker(self.symbol+'/USDT')['close']
        self.leverage = leverage
        self.amount = usdt / price * importance * self.leverage
        print(self.symbol)
        print(self.standard_long)
        print(self.addition_long)
        print(self.standard_short)
        print(self.addition_short)
        print(self.amount)
        
        positions = self.binance.fetch_balance()['info']['positions']
        for p in positions:
            if p['symbol'] == self.symbol+'USDT' and p['positionSide'] == 'LONG':
                print(float(p['positionAmt']))
                if float(p['positionAmt']) > 0:
                    self.amount_long = float(p['positionAmt'])
                else:
                    self.amount_long = self.amount
                    self.binance.create_order(symbol=self.symbol+'/USDT', side='buy', type="MARKET", amount=self.amount, params={'positionSide': 'long'})             
            elif p['symbol'] == self.symbol+'USDT' and p['positionSide'] == 'SHORT':
                print(float(p['positionAmt']))
                if float(p['positionAmt']) < 0:
                    self.amount_short = -float(p['positionAmt'])
                else:
                    self.amount_short = self.amount
                    self.binance.create_order(symbol=self.symbol+'/USDT', side='sell', type="MARKET", amount=self.amount, params={'positionSide': 'short'})
        
        time.sleep(0.2)  
        positions = self.binance.fetch_balance()['info']['positions']
        for p in positions:
            if p['symbol'] == self.symbol+'USDT' and p['positionSide'] == 'LONG':
                self.entry_price_long = float(p['entryPrice'])
            elif p['symbol'] == self.symbol+'USDT' and p['positionSide'] == 'SHORT':
                self.entry_price_short = float(p['entryPrice'])
        print(self.amount_long, self.amount_short)
        print(self.entry_price_long, self.entry_price_short)

    def update(self):
        
        price = self.binance.fetch_ticker(self.symbol+'/USDT')['close']
        roe_long = (price / self.entry_price_long - 1) * 100 * self.leverage
        roe_short = (price / self.entry_price_short - 1) * 100 * self.leverage
        roe_short = -roe_short
        print(self.symbol, roe_long, roe_short, self.standard_long, self.standard_short)
        
        if roe_long < self.standard_long:
            #amount = self.usdt / price * self.importance * self.leverage
            self.amount_long += self.amount
            self.standard_long += self.addition_long
            self.binance.create_order(symbol=self.symbol+'/USDT', side='buy', type="MARKET", amount=self.amount, params={'positionSide': 'long'})
            time.sleep(0.2)
            positions = self.binance.fetch_balance()['info']['positions']
            for p in positions:
                if p['symbol'] == self.symbol+'USDT' and p['positionSide'] == 'LONG':
                    self.entry_price_long = float(p['entryPrice'])
        elif roe_long > 100:
            self.binance.create_order(symbol=self.symbol+'/USDT', side='sell', type="MARKET", amount=self.amount_long, params={'positionSide': 'long'})
            #amount = self.usdt / price * self.importance * self.leverage
            self.amount_long = self.amount
            self.standard_long = self.standard_init_long
            self.binance.create_order(symbol=self.symbol+'/USDT', side='buy', type="MARKET", amount=self.amount, params={'positionSide': 'long'})
            time.sleep(0.2)
            positions = self.binance.fetch_balance()['info']['positions']
            for p in positions:
                if p['symbol'] == self.symbol+'USDT' and p['positionSide'] == 'LONG':
                    self.entry_price_long = float(p['entryPrice'])

        if roe_short < self.standard_short:
            #amount = self.usdt / price * self.importance * self.leverage
            self.amount_short += self.amount
            self.standard_short += self.addition_short
            self.binance.create_order(symbol=self.symbol+'/USDT', side='sell', type="MARKET", amount=self.amount, params={'positionSide': 'short'})
            time.sleep(0.2)
            positions = self.binance.fetch_balance()['info']['positions']
            for p in positions:
                if p['symbol'] == self.symbol+'USDT' and p['positionSide'] == 'SHORT':
                    self.entry_price_short = float(p['entryPrice'])
        elif roe_short > 100:
            self.binance.create_order(symbol=self.symbol+'/USDT', side='buy', type="MARKET", amount=self.amount_short, params={'positionSide': 'short'})
            #amount = self.usdt / price * self.importance * self.leverage
            self.amount_short = self.amount
            self.standard_short = self.standard_init_short
            self.binance.create_order(symbol=self.symbol+'/USDT', side='sell', type="MARKET", amount=self.amount, params={'positionSide': 'short'})
            time.sleep(0.2)
            positions = self.binance.fetch_balance()['info']['positions']
            for p in positions:
                if p['symbol'] == self.symbol+'USDT' and p['positionSide'] == 'SHORT':
                    self.entry_price_short = float(p['entryPrice'])

        return self.symbol + str(roe_long) + str(roe_short) + str(self.standard_long) + str(self.standard_short) + "\n"

        
