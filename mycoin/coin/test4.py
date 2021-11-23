import sys
#import matplotlib.pyplot as plt
import ccxt
import etc
#import numpy as np
import time
import math
import pyupbit
import etc

binance = ccxt.binance({
    'apiKey': 'nJtYtDJrAHnn52vW1SeMqUBwaVMc7Hl46wzbE1QAmH45V1w40ZHwXu1JzjUA1wsP',
    'secret': 'Tp03WrIfSQbyrjQHUsaIoGezf9fZs9md59LCcHinmdjd6BXhfpJuL7fj479wuHeD',
    'options': {
        'createMarketBuyOrderRequiresPrice' : False,
        'defaultType' : 'future',
    }
})
upbit = ccxt.upbit({
    'apiKey': 'usSJmCIHV9BoLM6fWVVIDuBPG2GmOX4HdGBr82xK',
    'secret': 'Qef86e7FYVuK3PjkP807DaxMiGKkkaCra7oCs1ub',
    'options': {
        'createMarketBuyOrderRequiresPrice' : False
    }
})
pu = pyupbit.PyUpbit()

"""
balance = binance.fetch_balance()
print(balance['TRX']['free'])

print(upbit.create_market_buy_order('TRX/KRW', 6000))
time.sleep(5)
balance = upbit.fetch_balance()
funding_fee = pu.get_funding_fee('TRX')
print(balance['TRX']['free'])
#print(upbit.create_market_sell_order('XRP/KRW', balance['XRP']['free']))
#print(upbit.has['fetchDepositAddress'])
#print(binance.has['createDepositAddress'])
#print(upbit.fetchDepositAddress('MED'))
address = binance.fetchDepositAddress('TRX')
max_balance = int((balance['TRX']['free'] - funding_fee) * 1e5) / 1e5
print(max_balance)
#print(binance.fetch_funding_fees()['withdraw']['XRP'])
print(upbit.withdraw('TRX', max_balance, address['address'], tag=address['tag']))
while True:
    time.sleep(3)
    withdrawals = upbit.fetch_withdrawals('TRX')
    deposits = binance.fetch_deposits('TRX')
    if withdrawals and deposits and withdrawals[-1]['txid'] == deposits[-1]['txid']:
        time.sleep(30)
        balance = binance.fetch_balance()
        print(balance['TRX']['free'])
        print(binance.create_market_sell_order('TRX/USDT', balance['TRX']['free']))
        break


#print(binance.fetch_funding_fees()['withdraw']['TRX'])



print(upbit.fetch_withdrawals())
print(binance.fetch_deposits()[0]['info']['txId'])
print(upbit.fetch_deposits())


l = []

print(upbit.fetch_withdrawals('TRX')[-1]['txid'] == binance.fetch_deposits('TRX')[-1]['txid'])
if not l:
    print(0)

    balance = binance.fetch_balance()

balance = binance.fetch_balance()
print(balance['TRX']['free'], balance['USDT']['free'])
#print(binance.create_market_buy_order('TRX/USDT', int(balance['USDT']['free']) * 0.999))
address = upbit.fetchDepositAddress('TRX')
print(address)
print(binance.withdraw('TRX', balance['TRX']['free'], address['address'], tag=address['tag']))

#print(binance.load_markets())
positions = binance.fetch_balance()['info']['positions']
for p in positions:
    if p['symbol'] == 'BTCUSDT':
        p['leverage'] = '2'
        pos = p

#print(binance.fetchOHLCV('BTC/USDT', '15m', limit=1))
print(binance.fetch_balance()['USDT']['free'])
print(pos)

#binance.create_order(symbol='BTC/USDT', side='sell', type="MARKET", amount=0.001)

candles = binance.fetchOHLCV("XRP/USDT", '15m', limit=16)
slow_k = etc.get_stocastic_slow_k(candles[-7:], 5, 3)
slow_k_before = etc.get_stocastic_slow_k(candles[-8:-1], 5, 3)
rsi = etc.get_rsi(candles[1:], 14)
rsi_before = etc.get_rsi(candles[:-1], 14)
print(slow_k, slow_k_before, rsi, rsi_before)

binance.create_order(symbol='XRP/USDT', side='buy', type="MARKET", amount=10, params={'positionSide': 'long'})
binance.create_order(symbol='XRP/USDT', side='sell', type="MARKET", amount=7, params={'positionSide': 'short'})
"""
print(binance.fetch_ticker('XRP/USDT')['close'])

#binance.create_order(symbol='XRP/USDT', side='buy', type="MARKET", amount=10, params={'positionSide': 'long'})
positions = binance.fetch_balance()['info']['positions']
for p in positions:
    if p['symbol'] == 'XRPUSDT' and p['positionSide'] == 'SHORT':
        pos = p

print(float(pos['positionAmt']))


n = -5
print(-n)