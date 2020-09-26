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

import time
from binance.websockets import BinanceSocketManager # Import the Binance Socket Manager
from twisted.internet import reactor


# Instantiate a BinanceSocketManager, passing in the client that you instantiated
bm = BinanceSocketManager(client)

# This is our callback function. For now, it just prints messages as they come.
def handle_message(msg):
    print('start delay')
    time.sleep(4)
    print('end delay')
    # print(msg)

# Start trade socket with 'ETHBTC' and use handle_message to.. handle the message.
conn_key = bm.start_trade_socket('ETHBTC', handle_message)
# then start the socket manager
bm.start()

# let some data flow..
# time.sleep(10)
print('start')
time.sleep(20)

print('end')


# stop the socket manager
bm.stop_socket(conn_key)
reactor.stop()
