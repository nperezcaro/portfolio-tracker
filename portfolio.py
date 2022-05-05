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


#Create functions to pull the diferent price of assets
def _get_asset_data(ticker, country, state=False):
    return investpy.stocks.get_stock_recent_data(ticker, country, state)


def _get_commodities_data(ticker):
    return investpy.commodities.get_commodity_recent_data(ticker)


def _get_currencycross_data(ticker):
    return investpy.currency_crosses.get_currency_cross_recent_data(ticker)


stocks = [
    ('Eco', 'Colombia'),
    ('JPM', 'United States'),
    ('TSM', 'United States'),
    ('CSCO', 'United States'),
    ('NVDA', 'United States'),
    ('BLK', 'United States'),
    ]

commodities = ['Gold']

exchange_rate = float(_get_currencycross_data('USD/COP').iloc[0,3])


results = []

for stock in stocks:
    result = _get_asset_data(*stock).iloc[0,3]
    results.append(result)

for commoditie in commodities:
    result = _get_commodities_data(commoditie).iloc[0,3]
    results.append(result)


price_assets_cop = []
for result in results:
    if result == results[:1]:
        price_assets_cop.append(result * 1)
    else:
        price_assets_cop.append(round(result * exchange_rate, 2))


amount_of_assets = [1.74, 5.29, 0.51, 45.65, 24.40, 46.77, 46.01]


#Profitability summary
net_financial_position = float(np.dot(price_assets_cop, amount_of_assets))
net_financial_position_text = moneyfmt(Decimal(float(np.dot(price_assets_cop, amount_of_assets))), 2, '$', ',')
print(f"The current value of the portfolio's asset position: {net_financial_position_text}")


relative_delta = (net_financial_position - initial_investment) / initial_investment
absolute_delta = net_financial_position - initial_investment
print('This implies the following variation:')
print(f'Relative Delta:','{percent:.2%}'.format(percent=relative_delta))
print(f'Absolute Delta:', moneyfmt(Decimal(absolute_delta), 2, '$', ','))