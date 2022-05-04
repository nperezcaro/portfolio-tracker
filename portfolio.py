#Import all the packages that will be used
import investpy
import pandas as pd
import requests
import numpy as np
from decimal import *

initial_investment = 150000000

#Function to use money format in some numbers
    #Retrieved from https://aztrock.blogspot.com/2013/10/convertir-decimal-formato-de-dinero.html
def moneyfmt(value, places=2, curr='', sep=',', dp='.', pos='', neg='-', trailneg=''):

    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    if places:
        build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


#Function that will be use to call the stock price from Ferrari and Square
def get_stock_price(ticker_symbol, api):
    url = f"https://api.twelvedata.com/price?symbol={ticker_symbol}&apikey={api}"
    response = requests.get(url).json()
    price = response['price']
    return(price)


ticker = 'RACE'
ticker_1 = 'SQ'
api_key = '6dfc647b94304214a16389174d0a47f8'