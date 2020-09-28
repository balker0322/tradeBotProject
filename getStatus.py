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

price = {'BTCUSDT': pd.DataFrame(columns=[ 	'e', # Event type
							   				'E', # Event time
							   				's', # Symbol
							   				'p', # Price change
							   				'P', # Price change percent
							   				'w', # Weighted average price
							   				'x', # Previous day's close price
							   				'c', # Current day's close price
							   				'Q', # Close trade's quantity
							   				'b', # Best bid price
							   				'B', # Bid bid quantity
							   				'a', # Best ask price
							   				'A', # Best ask quantity
							   				'o', # Open price
							   				'h', # High price
							   				'l', # Low price
							   				'v', # Total traded base asset volume
							   				'q', # Total traded quote asset volume
							   				'O', # Statistics open time
							   				'C', # Statistics close time
							   				'F', # First trade ID
							   				'L', # Last trade Id
							   				'n', # Total number of trades
										]), 'error':False}

def btc_pairs_trade(msg):		
	# define how to process incoming WebSocket messages
	if msg['e'] != 'error':
		log = pd.DataFrame({x:[msg[x]] for x in msg})
		log.to_csv(pairs+'.csv', header = False, mode = 'a')
	else:
		price['error']:True

# init and start the WebSocket
bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket(pairs, btc_pairs_trade)
bsm.start()

while(True):
	pass