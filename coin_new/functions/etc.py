import requests
import json

def get_exchange_rate():
    url = "http://data.fixer.io/api/latest?access_key=633e030f429629ba29b17b68218f1277"
    response = requests.request("GET", url)
    #print(response.text)
    json_data = json.loads(response.text)

    return json_data["rates"]["KRW"] / json_data["rates"]["USD"]

def get_noise_avg(candle):
    windows = len(candle)-1
    noise_sum = 0
    for i in range(windows):
        noise_sum += 1 - abs(candle[i][1]- candle[i][4]) / (candle[i][2]- candle[i][3])
    noise_avg = noise_sum / windows
    return noise_avg

def filtering(informs, limit):
    res = dict()
    #print(informs)
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

def get_stocastic_fast_k(candles):
    high = -1
    low = 1e9
    now = candles[-1][4]
    for candle in candles:
        if candle[2] > high:
            high = candle[2]
        if candle[3] < low:
            low = candle[3]
    return (now - low) / (high - low) * 100

def get_stocastic_slow_k(candles, n, m):
    avg = 0
    for i in range(m):
        avg += get_stocastic_fast_k(candles[i:i+n])
    avg /= m
    return avg

def get_stocastic_slow_d(candles, n, m, t):
    avg = 0
    for i in range(t):
        slow_k = get_stocastic_slow_k(candles[i:i+n+m-1], n, m)
        avg += slow_k
    avg /= t
    return avg, slow_k

def get_cci_M(high, low, close):
    return (high + low + close) / 3

def get_cci_m(candles):
    avg = 0
    for candle in candles:
        M = get_cci_M(candle[2], candle[3], candle[4])
        avg += M
    m = avg / len(candles)
    return M, m

def get_cci_d(candles, n):
    avg = 0
    for i in range(n):
        M, m = get_cci_m(candles[i:i+n])
        avg += abs(M-m)
    d = avg / n
    return M, m, d

def get_cci(candles, n):
    M, m, d = get_cci_d(candles, n)
    cci = (M - m) / (d * 0.015)
    #print(M, m, d)
    return cci

def get_rsi(candles, n):
    if len(candles) != n+1:
        return None

    au = 0
    ad = 0
    count_up = 0
    count_down = 0

    for i in range(n):
        if candles[i+1][4] > candles[i][4]:
            count_up += 1
            au += candles[i+1][4] - candles[i][4]
        else:
            count_down += 1
            ad += candles[i][4] - candles[i+1][4]
    if count_up > 0:
        au = au / count_up
    if count_down > 0:
        ad = ad / count_down
    rsi = au / (au + ad) * 100

    return rsi

def get_rsi_ma(candles, n, m):

    if len(candles) != n+m:
        return None

    avg = 0
    for i in range(m):
        avg += get_rsi(candles[i:i+n+1], n)
    avg /= m

    return avg

