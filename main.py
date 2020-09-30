from security import get_keys
from time import sleep
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import pandas as pd
import numpy as np
import os

keys = get_keys('client')
client = Client(keys['api_key'], keys['api_secret'])
trade_coin = 'BTC'
stable_coin = 'USDT'
pairs = trade_coin + stable_coin
binance_socket_error = False
trading_quantity = 0.00433
initial_asset = 0.0

def btc_pairs_trade(msg):		
	if msg['e'] != 'error':
		log = pd.DataFrame({x:[msg[x]] for x in msg})
		mode = 'w'
		if os.path.exists(pairs+'.csv'):
			mode = 'a'
		log.to_csv(pairs+'.csv', header = False, mode = mode)
	else:
		binance_socket_error = True

def get_status(seconds):
	df = pd.read_csv(pairs+'.csv', header=None, usecols=[2,8])
	df = df.rename(columns={2: "date", 8: "price"})
	df.date = pd.to_datetime(df.date, unit='ms')
	start_time = df.date.iloc[-1] - pd.Timedelta(seconds=seconds)
	return df.loc[df.date >= start_time]

def get_action(status):
	average = [5, 10, 20]
	try:	
		ma = [MA(seconds=seconds*60, status=status) for seconds in average]
		print(["{0:.2f}".format(x) for x in ma])
	except:
		return 0
	if ma[0] > ma[1] and ma[1] > ma[2]: # buy
		return 1
	if ma[0] < ma[1] and ma[1] < ma[2]: # sell
		return 2
	return 0

def MA(seconds, status):
	start_time = status.date.iloc[-1] - pd.Timedelta(seconds=seconds)
	df = status.loc[status.date >= start_time]
	return df.price.mean()

def buy_coin():
	client.create_order(symbol=pairs, side='BUY', type='MARKET', quantity=trading_quantity)

def sell_coin():
	client.create_order(symbol=pairs, side='SELL', type='MARKET', quantity=trading_quantity)

def get_total_asset(coin_list, base_coin):
	total_asset = 0.0
	for coin_symbol in coin_list:
		pair = coin_symbol + base_coin
		if coin_symbol == base_coin:
			total_asset += float(client.get_asset_balance(coin_symbol,recvWindow=10000)['free'])
			continue
		total_asset += float(client.get_asset_balance(coin_symbol,recvWindow=10000)['free']) * float(client.get_symbol_ticker(symbol=pair)['price'])
	return total_asset

def display_result(initial_asset, action_display):
	try:
		current_asset = get_total_asset(coin_list = ['BTC', 'BNB', 'USDT'], base_coin = 'USDT')
		gain = (current_asset/initial_asset) - 1.0
		gain *= 100.0
		display =  ("-" if gain < 0 else "+") + "{0:.4f} % ".format(abs(gain)) + action_display
		print(display)
	except:
		pass

bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket(pairs, btc_pairs_trade)
bsm.start()

while True:
	try:
		initial_asset = get_total_asset(coin_list = ['BTC', 'BNB', 'USDT'], base_coin = 'USDT')
		break
	except:
		pass

# sleep(21*60)

action_display = ''
loop_count = 0
next_action = 'BUY'

while True:
	
	if loop_count == 0:
		display_result(initial_asset = initial_asset, action_display = action_display)
		loop_count = 10*60*5
	loop_count -= 1
	action_display = ''
	
	if binance_socket_error:
		bsm.stop_socket(conn_key)
		bsm.start()
		binance_socket_error = False
	else:
		try:
			status = get_status(seconds = 21*60) # get status of previous n seconds
			action = get_action(status = status)
		except:
			print('error in get status / action')
			continue

		if action == 1 and next_action == 'BUY':
			try:
				action_display = ''
				print('trying to buy ...')
				buy_coin()
				print('done buy')
				display_result(initial_asset = initial_asset, action_display = action_display)
				next_action = 'SELL'
			except:
				next_action = 'BUY'
				continue

		elif action == 2 and next_action == 'SELL':
			try:
				action_display = ''
				print('trying to sell ...')
				sell_coin()
				print('done sell')
				display_result(initial_asset = initial_asset, action_display = action_display)
				next_action = 'BUY'
			except:
				next_action = 'SELL'
				continue
	
	sleep(0.1)