import time

def get_candles(binance, market, unit, limit):
    while True:
        try:
            return binance.fetchOHLCV(market+'/USDT', unit, limit=limit)
        except Exception as e:
            print('get_candles_except', e)
            time.sleep(3)
            continue

def get_usdt(binance):
    while True:
        try:
            return binance.fetch_balance()['USDT']['free']
        except Exception as e:
            print('get_usdt_except', e)
            time.sleep(3)
            continue

def long_in(binance, market, amount):
    while True:
        try:
            binance.create_order(symbol=market+'/USDT', side='buy', type="MARKET", amount=amount, params={'positionSide': 'long'})
            break
        except:
            print("long_in_except")
            time.sleep(3)
            continue

def long_out(binance, market, amount):
    while True:
        try:
            binance.create_order(symbol=market+'/USDT', side='sell', type="MARKET", amount=amount, params={'positionSide': 'long'})
            break
        except:
            print("long_out_except")
            time.sleep(3)
            continue

def short_in(binance, market, amount):
    while True:
        try:
            binance.create_order(symbol=market+'/USDT', side='sell', type="MARKET", amount=amount, params={'positionSide': 'short'})
            break
        except:
            print("short_in_except")
            time.sleep(3)
            continue

def short_out(binance, market, amount):
    while True:
        try:
            binance.create_order(symbol=market+'/USDT', side='buy', type="MARKET", amount=amount, params={'positionSide': 'short'})
            break
        except:
            print("short_out_except")
            time.sleep(3)
            continue