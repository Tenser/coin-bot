class Coin:
    def __init__(self, market, upbit_price, binance_price, kp, rp):
        self.kp = kp
        self.rp = rp
        self.market = market
        self.upbit_price = upbit_price    
        self.binance_price = binance_price
        self.sign = 0
        self.rate = upbit_price / binance_price
        if self.rate > self.kp:
            self.sign = 1
        elif self.rate < self.rp:
            self.sign = -1
            
    def update(self, upbit_price, binance_price):
        
        self.upbit_price = upbit_price    
        self.binance_price = binance_price
        self.rate = upbit_price / binance_price
        
        if self.rate > self.kp:
            self.sign = 1
        elif self.rate < self.rp:
            self.sign = -1
        else:
            self.sign = 0

    
        