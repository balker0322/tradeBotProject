from security import get_keys
from time import sleep
# from binanceSimple import sellAmount, buyAmount
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import pandas as pd
import numpy as np
# from sklearn.linear_model import LinearRegression

pairs = 'BTCUSDT'

x = get_keys('client')
client = Client(x['api_key'], x['api_secret'])


csvdata = pd.read_csv("BTCUSDT.csv", header=None, usecols=[2,8])
csvdata = csvdata.rename(columns={2: "date", 8: "price"})
csvdata.date = pd.to_datetime(csvdata.date, unit='ms')

price = {'BTCUSDT': csvdata, 'error':False}

# price = {'BTCUSDT': pd.DataFrame(columns=['date', 'price']), 'error':False}

def btc_pairs_trade(msg):		
	# define how to process incoming WebSocket messages
	if msg['e'] != 'error':
		log = pd.DataFrame({x:[msg[x]] for x in msg})
		log.to_csv(pairs+'.csv', header = False, mode = 'a')
		dateStamp = pd.Timestamp.now()
		price['BTCUSDT'].loc[len(price['BTCUSDT'])] = [dateStamp, float(msg['c'])]
	else:
		price['error']:True

def buyAmount(coin, pair):
	balanceBuy = float(client.get_asset_balance(coin,recvWindow=10000)['free'])
	close = float(client.get_symbol_ticker(symbol=pair)['price'])
	maxBuy = round(balanceBuy / close * .995, 5)
	return maxBuy
	
def sellAmount(coin):
	balanceSell = float(client.get_asset_balance(coin,recvWindow=10000)['free'])
	maxSell = round(balanceSell * .995, 5)
	return maxSell

def MA(sec):
	df = price['BTCUSDT']
	start_time = df.date.iloc[-1] - pd.Timedelta(seconds=sec)
	df = df.loc[df.date >= start_time]
	return df.price.mean()

# init and start the WebSocket
bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket(pairs, btc_pairs_trade)
bsm.start()

# for i in range(15):
# 	print(15 - i, 'minutes remaining...')
# 	sleep(60)

# print('last 10 seconds...')
# sleep(10)
# sleep(40)

while True:

	metric = 0.0

	# try:
	# 	maxsell = sellAmount('BTC')
	# 	maxbuy = buyAmount('USDT', 'BTCUSDT')
	# except:
	# 	pass

	# error check to make sure WebSocket is working
	if price['error']:
		print("price['error']")
		# stop and restart socket
		bsm.stop_socket(conn_key)
		bsm.start()
		price['error'] = False
	else:
		try:
			metric = (MA(30) / MA(900)) - 1.0
			# metric = (MA(5) / MA(30)) - 1.0
			metric*=100
		except:
			print('MA error')
			metric = 0.0
			continue
		
		print('MA(30) / MA(900):', round(metric, 4), '%')

		if metric > 0.1:
			try:
				print('BUY')
				client.create_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity=0.00433)
			except:
				pass
			continue
		elif metric < -0.1:
			try:
				print('SELL')
				client.create_order(symbol='BTCUSDT', side='SELL', type='MARKET', quantity=0.00433)
			except:
				pass
			continue
	sleep(0.1)






















# from security import get_keys
# from time import sleep
# from binanceSimple import sellAmount, buyAmount

# from binance.client import Client
# from binance.exceptions import BinanceAPIException, BinanceOrderException
# from binance.websockets import BinanceSocketManager
# from twisted.internet import reactor
# import pandas as pd
# import numpy as np
# from sklearn.linear_model import LinearRegression

# x = get_keys('client')
# client = Client(x['api_key'], x['api_secret'])

# # init
# price = {'BTCUSDT': pd.DataFrame(columns=['date', 'price']), 'error':False}
# maxsell = 0
# maxbuy = 0

# loading_disp = True

# def MA(sec):
#     data = pd.read_csv("BTCUSDT.csv", header=None, usecols=[2,8])
#     start_time = pd.to_datetime(data[2], unit='ms').iloc[-1] - pd.Timedelta(seconds=sec)
#     data[2] = pd.to_datetime(data[2], unit='ms')
#     x = data.loc[data[2] >= start_time]
#     x = x[8].mean()
#     return x

# def btc_pairs_trade(msg):		
# 	# define how to process incoming WebSocket messages
# 	if msg['e'] != 'error':
# 		dateStamp = pd.Timestamp.now()
# 		price['BTCUSDT'].loc[len(price['BTCUSDT'])] = [dateStamp, float(msg['c'])]
# 		print(dateStamp)
# 	else:
# 		price['error']:True

# # init and start the WebSocket
# bsm = BinanceSocketManager(client)
# conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_pairs_trade)
# bsm.start()

# ## main
# while len(price['BTCUSDT']) == 0:
# 	# wait for WebSocket to start streaming data
# 	sleep(0.1)

# print('Gathering initial data...')	
# sleep(60.0*float(10))
# print('Done gathering initial data.')	
# loading_disp = False

# while True:

# 	try:
# 		maxsell=sellAmount('BTC')
# 		maxbuy=buyAmount('USDT', 'BTCUSDT')
# 	except:
# 		pass

# 	# error check to make sure WebSocket is working
# 	if price['error']:
# 		# stop and restart socket
# 		bsm.stop_socket(conn_key)
# 		bsm.start()
# 		price['error'] = False
# 	else:
# 		# df = price['BTCUSDT']
# 		# start_time = df.date.iloc[-1] - pd.Timedelta(minutes=1)
# 		# df = df.loc[df.date >= start_time]
# 		# max_price = df.price.max()
# 		# min_price = df.price.min()
# 		df = price['BTCUSDT']

# 		# y = np.array(disp['Close'].astype(float))
# 		# # x = np.array(disp['Close time'].astype(float)).reshape((-1, 1))
# 		# x = np.linspace(0.0, float(min_num) - 1.0, num = min_num).reshape((-1, 1))
# 		# slope = LinearRegression().fit(x, y).coef_

# 		# percentage_change = 0.02
		
# 		# if df.price.iloc[-1] < max_price * (1.0 - percentage_change):
# 		# 	print('current price < max_price *', 1.0 - percentage_change)
# 		# 	try:
# 		# 		order = client.create_test_order(symbol='BTCUSDT', side='SELL', type='MARKET', quantity = maxsell)
# 		# 		print('Sell BTC:', maxsell)
# 		# 		print('Asset:', maxsell + maxbuy)
# 		# 		break
# 		# 	except BinanceAPIException as e:
# 		# 		# error handling goes here
# 		# 		print(e)
# 		# 	except BinanceOrderException as e:
# 		# 		# error handling goes here
# 		# 		print(e)

# 		# elif df.price.iloc[-1] > min_price * (1.0 + percentage_change):
# 		# 	print('current price > min_price *', 1.0 + percentage_change)
# 		# 	try:
# 		# 		order = client.create_test_order(symbol='BTCUSDT', side='BUY', type='MARKET', quantity=maxbuy)
# 		# 		print('Buy BTC:', maxbuy)
# 		# 		print('Asset:', maxsell + maxbuy)
# 		# 		break
# 		# 	except BinanceAPIException as e:
# 		# 		# error handling goes here
# 		# 		print(e)
# 		# 	except BinanceOrderException as e:
# 		# 		# error handling goes here
# 		# 		print(e)
# 	sleep(0.1)
