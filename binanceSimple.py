from binance.client import Client
from security import get_keys

x = get_keys('client')
client = Client(x['api_key'], x['api_secret'])

def buyAmount(coin, pair):
    balanceBuy = float(client.get_asset_balance(coin,
    recvWindow=10000)['free'])
    close = float(client.get_symbol_ticker(symbol=pair)['price'])
    maxBuy = round(balanceBuy / close * .995, 5)
    return maxBuy
    
def sellAmount(coin):
    balanceSell = float(client.get_asset_balance(coin,
    recvWindow=10000)['free'])
    maxSell = round(balanceSell * .995, 5)
    return maxSell
    
def buy(amount, pair):
    client.create_test_order(
    symbol=pair,
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_MARKET,
    quantity=amount,
    recvWindow=10000)
    print('Buy: {}'.format(amount))
    
def sell(amount, pair):
    client.create_test_order(
    symbol=pair,
    side=Client.SIDE_SELL,
    type=Client.ORDER_TYPE_MARKET,
    quantity=amount,
    recvWindow=10000)
    print('Sell: {}'.format(amount))

# maxBuy = buyAmount('ETH', 'USDTETH')
# buy(maxBuy, 'ETHUSDT')
# maxSell = sellAmount('ETH')
# sell(maxSell, 'ETHUSDT')

'''
interval2(i2) > interval1(i1)
closingPrice (cp)

get status
    if increasing >> return hi
        cp(i1) > cp(i2)
    if decreasing >> return lo
        cp(i1) < cp(i2)

infinite loop
    status = get status
    if status == low AND next action == buy:
        buy
        set next action = sell
    if status == hi AND next action == sell:
        sell
        set next action = buy
    otherwise hold
'''

def get_historical_closing_average(minute_ago):
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, str(minute_ago) + " min ago UTC")
    average = 0.0
    for point in klines:
        average += float(point[4])
    return average / float(len(klines))

def get_current_price():
    return float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])


# maxBuy = buyAmount('ETH', 'USDTETH')
# buy(maxBuy, 'ETHUSDT')
# maxSell = sellAmount('ETH')
# sell(maxSell, 'ETHUSDT')

# print('buyAmount:', buyAmount('BTC', 'BTCUSDT'))
# print('sellAmount', sellAmount('BTC'))
# print(buy(0.0, 'ETHUSDT'))
