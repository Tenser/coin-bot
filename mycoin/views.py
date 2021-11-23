from django.http import HttpResponse
from mycoin.coin.dual import DualPosition



dp = DualPosition([{'symbol': 'ETH', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1600, 'additionShort': -400}, 
                    {'symbol': 'XRP', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'XLM', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1600, 'additionShort': -400},
                    {'symbol': 'ADA', 'standardLong': -400, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'BCH', 'standardLong': -400, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'EOS', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'LTC', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'TRX', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'ETC', 'standardLong': -400, 'additionLong': -200, 'standardShort': -1600, 'additionShort': -400},
                    {'symbol': 'LINK', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1600, 'additionShort': -400},
                    {'symbol': 'VET', 'standardLong': -400, 'additionLong': -200, 'standardShort': -2000, 'additionShort': -400},
                    {'symbol': 'NEO', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1600, 'additionShort': -400},
                    {'symbol': 'XMR', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'DASH', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'ZEC', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'XTZ', 'standardLong': -400, 'additionLong': -200, 'standardShort': -1600, 'additionShort': -400},
                    {'symbol': 'ATOM', 'standardLong': -1400, 'additionLong': -200, 'standardShort': -1600, 'additionShort': -400},
                    {'symbol': 'ONT', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'BAT', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400},
                    {'symbol': 'QTUM', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1600, 'additionShort': -400},
                    {'symbol': 'THETA', 'standardLong': -600, 'additionLong': -200, 'standardShort': -2400, 'additionShort': -400},
                    {'symbol': 'ALGO', 'standardLong': -400, 'additionLong': -200, 'standardShort': -1600, 'additionShort': -400},
                    {'symbol': 'ZIL', 'standardLong': -400, 'additionLong': -200, 'standardShort': -2000, 'additionShort': -400},
                    {'symbol': 'ZRX', 'standardLong': -1400, 'additionLong': -200, 'standardShort': -1600, 'additionShort': -400},
                    {'symbol': 'SXP', 'standardLong': -200, 'additionLong': -200, 'standardShort': -1200, 'additionShort': -400}], 1900, 0.0007, 50)
"""
                    
"""                   
                    
def start(request):
    if dp.turn:
        return HttpResponse('already start')
    dp.turn = True
    dp.run()
    return HttpResponse('start success')

def end(request):
    dp.turn = False
    dp.log = ''
    return HttpResponse('end')

def check(request):
    return HttpResponse(dp.log)