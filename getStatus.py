from binance.client import Client
from security import get_keys

x = get_keys('client')
client = Client(x['api_key'], x['api_secret'])

def totalAssetBTC():
    totalBTC = 0.0
    for x in client.get_account()['balances']:
        baseCoin = 'BTC'
        freeBalance = float(x['free'])
        if freeBalance != 0.0:
            symbol = x['asset']
            exchangeSymbol = symbol + baseCoin
            exchangeRate = float(client.get_symbol_ticker(symbol=exchangeSymbol)['price'])
            totalBTC = totalBTC + exchangeRate*freeBalance
    
    return totalBTC

if __name__ == "__main__":
    old = totalAssetBTC() * float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])
    new = 0.0
    while(True):
        new = totalAssetBTC() * float(client.get_symbol_ticker(symbol="BTCUSDT")['price'])
        displayText = str(round(new,4)) + ' USDT '

        percentChange = (new / old) - 1.0
        percentChange *= 100

        if percentChange > 0.0:
            displayText += '  UP +'
        else:
            displayText += 'DOWN '
            
        
        displayText += str(round(percentChange,4)) + ' %'

        print(displayText)

        old = new