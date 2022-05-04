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


get_stock_price(ticker, api_key)
get_stock_price(ticker_1,api_key)


#Import price of the other assets using Investpy
    #The prices of the other two stocks (above) could not be imported with Investpy
df_1 = investpy.stocks.get_stock_recent_data('Eco','Colombia',False)
df_2 = investpy.stocks.get_stock_recent_data('JPM','United States',False)
df_3 = investpy.stocks.get_stock_recent_data('TSM','United States',False)
df_5 = investpy.stocks.get_stock_recent_data('CSCO','United States',False)
df_6 = investpy.commodities.get_commodity_recent_data('Gold')
df_8 = investpy.stocks.get_stock_recent_data('NVDA','United States',False)
df_9 = investpy.stocks.get_stock_recent_data('BLK','United States',False)
trm = investpy.currency_crosses.get_currency_cross_recent_data('USD/COP')


#Conversion of prices (they come as dataframes) to variables in order to perform operations
price_ecopetrol = df_1.iloc[0,3]
price_jpmorgan = df_2.iloc[0,3]
price_tsm = df_3.iloc[0,3]
price_ferrari = float(get_stock_price(ticker, api_key))
price_cisco = df_5.iloc[0,3]
price_gold = df_6.iloc[0,3]
price_square = float(get_stock_price(ticker_1, api_key))
price_nvidia = df_8.iloc[0,3]
price_blackrock = df_9.iloc[0,3]
price_usd = trm.iloc[0,3]


price_assets = [price_ecopetrol, price_jpmorgan, price_tsm, price_ferrari, price_cisco, price_gold, price_square, price_nvidia, price_blackrock]


price_assets_cop = []
for i in price_assets:
    if i == price_ecopetrol:
        price_assets_cop.append(i * 1)
    else:
        price_assets_cop.append(round(i * price_usd, 2))

print(price_assets_cop)