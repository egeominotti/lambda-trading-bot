import os
from chalice import Chalice
from chalicelib.exchange import Spot
import datetime
import json

app = Chalice(app_name='bot')
app.debug = True


def savehistory(data):
    json_object = json.dumps(data, indent=4)
    write_file_name = "/tmp/history_" + data.get('user') + '_' + data.get('ticker') + '.json'
    with open(write_file_name, "w") as outfile:
        outfile.write(json_object)
        outfile.close()

def readhistory(data):
    read_file_name = "/tmp/history_" + data.get('user') + '_' + data.get('ticker') + '.json'
    with open(read_file_name, 'r') as f:
        data_loaded = json.load(f)
        buy_balance = data_loaded.get('qty')
        app.log.debug(data_loaded)
        f.close()
    os.remove(read_file_name)

    return {'balance': buy_balance}

def tradespot(value):

    api_key = value.get('api_key')
    api_secret = value.get('api_secret')
    ticker = value.get('ticker')
    asset = value.get('asset')
    action = value.get('action')
    user = value.get('user')
    telegram = value.get('telegram')

    try:
        exchange = Spot(api_key=api_key,
                        api_secret=api_secret,
                        symbol=ticker,
                        asset=asset)

        # buy
        if action == 'buy':

            balance = round(exchange.getFreeAssetBalance(), 3)
            order_buy = exchange.buy()
            app.log.debug("Order buy: " + str(order_buy))
            if isinstance(order_buy, dict):

                executedQty = float(order_buy.get('executedQty'))


                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                message = "Buy Spot: " + str(ticker) + " 📈 " + \
                          "\n" + "User: " + user + \
                          "\n" + "Market Spot" \
                          "\n" + "Buy Price: " + str(exchange.getCurrentPrice()) + "$" \
                          "\n" + "Quantity: " + str(round(executedQty, exchange.getSymbolPrecision())) + \
                          "\n" + "Start trade quantity: " + str(balance) + " " + asset + \
                          "\nDate: " + str(now)

                telegram.send(message)

                data = {
                    'user': user,
                    'orderId': order_buy.get('orderId'),
                    'qty': balance,
                    'asset': asset,
                    'ticker': ticker
                }

                # thread = Thread(target=savehistory, args=(data,))
                # thread.daemon = True
                # thread.start()
                # status = thread.join()
                # app.log.debug(status)

            # Se l'ordine non è un dizionario allora non è stato creato
            if isinstance(order_buy, Exception):
                message = "⛔ " + user.upper() + " non posso comprare, risultano eseerci " + str(
                    round(exchange.getFreeAssetBalance(),
                          2)) + " " + asset + " nel tuo account è necessaria una quantità maggiore di 10."
                telegram.send(message)

        # sell
        if action == 'sell':

            order_sell = exchange.sell()
            app.log.debug("Order sell: " + str(order_sell))

            if isinstance(order_sell, dict):

                balance = round(exchange.getFreeAssetBalance(), 3)
                executedQty = float(order_sell.get('executedQty'))

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                data = {
                    'user': user,
                    'ticker': ticker
                }

                # thread = Thread(target=readhistory, args=(data,))
                # thread.daemon = True
                # thread.start()
                # return_value = thread.join()
                # qty = return_value.get('balance')

                message = "Sell Spot: " + str(ticker) + " ✅ " + \
                          "\n" + "User: " + user + \
                          "\n" + "Market Spot" \
                          "\n" + "Sell Price: " + str(exchange.getCurrentPrice()) + "$" \
                          "\n" + "Quantity: " + str(round(executedQty, exchange.getSymbolPrecision())) + \
                          "\n" + "Balance: " + str(round(balance,2)) + " " + asset +\
                          "\nDate: " + str(now)

                telegram.send(message)

            if isinstance(order_sell, Exception):
                message = "⛔ " + user.upper() + " non posso vendere, risultano eseerci " + str(
                    round(exchange.getFreePairBalance(),
                          exchange.getSymbolPrecision())) + " " + ticker + " nel tuo account, che sono inferiori a 10$"
                telegram.send(message)

    except Exception as e:
        message = "Error: " + str(e)
        telegram.send(message)
