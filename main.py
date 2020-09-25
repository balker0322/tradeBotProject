from binance.client import Client
from security import get_keys

x = get_keys('client')
client = Client(x['api_key'], x['api_secret'])

# for x in client.get_symbol_ticker():
#     if 'USD' in x['symbol']:
#         print(x['symbol'])

# exchangeRateBTCUSDT = client.get_symbol_ticker(symbol="BTCUSDT")['price']
# exchangeRateBTCUSDT = float(exchangeRateBTCUSDT)

# for x in client.get_account()['balances']:
#     assetPrice = float(x['free'])
#     if assetPrice != 0.0:
#         symbol = x['asset'] + 'BTC'
#         exchangeRate = client.get_symbol_ticker(symbol=symbol)['price']
#         exchangeRate = float(exchangeRate)
#         print (x['asset'], assetPrice*exchangeRate*exchangeRateBTCUSDT*50.0, 'PHP')
