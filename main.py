from security import get_keys
from time import sleep
from binanceSimple import sellAmount, buyAmount

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

x = get_keys('client')
client = Client(x['api_key'], x['api_secret'])

# init
price = {'BTCUSDT': pd.DataFrame(columns=['date', 'price']), 'error':False}
maxsell = 0
maxbuy = 0

loading_disp = True

def btc_pairs_trade(msg):		
	# define how to process incoming WebSocket messages
	if msg['e'] != 'error':
		dateStamp = pd.Timestamp.now()
		price['BTCUSDT'].loc[len(price['BTCUSDT'])] = [dateStamp, float(msg['c'])]
		print(dateStamp)
	else:
		price['error']:True

# init and start the WebSocket
bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_pairs_trade)
bsm.start()

## main
while len(price['BTCUSDT']) == 0:
	# wait for WebSocket to start streaming data
	sleep(0.1)

print('Gathering initial data...')	
sleep(60.0*float(10))
print('Done gathering initial data.')	
loading_disp = False

while True:

	try:
		maxsell=sellAmount('BTC')
		maxbuy=buyAmount('USDT', 'BTCUSDT')
	except:
		pass

	# error check to make sure WebSocket is working
	if price['error']:
		# stop and restart socket
		bsm.stop_socket(conn_key)
		bsm.start()
		price['error'] = False
	else:
		# df = price['BTCUSDT']
		# start_time = df.date.iloc[-1] - pd.Timedelta(minutes=1)
		# df = df.loc[df.date >= start_time]
		# max_price = df.price.max()
		# min_price = df.price.min()
		df = price['BTCUSDT']

		start_time = df.date.iloc[-1] - pd.Timedelta(minutes=9)
		df_a = df.loc[df.date >= start_time]
		y = np.array(df_a.price)
		x = np.array(df_a.date).reshape(-1, 1)
		slope9 = LinearRegression().fit(x, y).coef_

		
		start_time = df.date.iloc[-1] - pd.Timedelta(minutes=6)
		df_a = df.loc[df.date >= start_time]
		y = np.array(df_a.price)
		x = np.array(df_a.date).reshape(-1, 1)
		slope6 = LinearRegression().fit(x, y).coef_

		
		start_time = df.date.iloc[-1] - pd.Timedelta(minutes=3)
		df_a = df.loc[df.date >= start_time]
		y = np.array(df_a.price)
		x = np.array(df_a.date).reshape(-1, 1)
		slope3 = LinearRegression().fit(x, y).coef_

		print(slope9, slope6, slope3)

		# y = np.array(disp['Close'].astype(float))
		# # x = np.array(disp['Close time'].astype(float)).reshape((-1, 1))
		# x = np.linspace(0.0, float(min_num) - 1.0, num = min_num).reshape((-1, 1))
		# slope = LinearRegression().fit(x, y).coef_

		# percentage_change = 0.02
		
		# if df.price.iloc[-1] < max_price * (1.0 - percentage_change):
		# 	print('current price < max_price *', 1.0 - percentage_change)
		# 	try:
		# 		order = client.create_test_order(symbol='BTCUSDT', side='SELL', type='MARKET', quantity = maxsell)
		# 		print('Sell BTC:', maxsell)
		# 		print('Asset:', maxsell + maxbuy)
		# 		break
		# 	except BinanceAPIException as e:
		# 		# error handling goes here
		# 		print(e)
		# 	except BinanceOrderException as e:
		# 		# error handling goes here
		# 		print(e)

		# elif df.price.iloc[-1] > min_price * (1.0 + percentage_change):
		# 	print('current price > min_price *', 1.0 + percentage_change)
		# 	try:
		# 		order = client.create_test_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity=maxbuy)
		# 		print('Buy BTC:', maxbuy)
		# 		print('Asset:', maxsell + maxbuy)
		# 		break
		# 	except BinanceAPIException as e:
		# 		# error handling goes here
		# 		print(e)
		# 	except BinanceOrderException as e:
		# 		# error handling goes here
		# 		print(e)
	sleep(0.1)
