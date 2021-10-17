import sys
from chalice import Chalice

from chalicelib.exchange import Spot
import datetime
app = Chalice(app_name='bot')
app.debug = True

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

            order_buy = exchange.buy()
            app.log.debug("Order buy: " + str(order_buy))
            if isinstance(order_buy, dict):
                balance = round(exchange.getBalance(), 3)

                executedQty = float(order_buy.get('executedQty'))
                #commission = float(order_buy.get('fills')[0]['commission'])
                #commissionAsset = order_buy.get('fills')[0]['commissionAsset']

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                message = "Buy Spot: " + str(ticker) + " 📈 " + \
                          "\n" + "User: " + user + \
                          "\n" + "Market Spot" \
                          "\n" + "Buy Price: " + str(exchange.getCurrentPrice()) + \
                          "\n" + "Quantity: " + str(round(executedQty, exchange.getSymbolPrecision())) + \
                          "\nDate: " + str(now)

                telegram.send(message)

            # Se l'ordine non è un dizionario allora non è stato creato
            if not isinstance(order_buy, dict):
                message = "⛔ " + user.upper() + " non posso comprare, risultano eseerci " + str(
                    round(exchange.getFreeAssetBalance(),
                          2)) + " " + asset + " nel tuo account è necessaria una quantità maggiore di 10."
                telegram.send(message)

        # sell
        if action == 'sell':

            order_sell = exchange.sell()
            app.log.debug("Order sell: " + str(order_sell))
            if isinstance(order_sell, dict):

                balance = round(exchange.getBalance(), 3)

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                message = "Sell Spot: " + str(ticker) + " ✅ " + \
                          "\n" + "User: " + user + \
                          "\n" + "Market Spot" \
                          "\n" + "Sell Price: " + str(exchange.getCurrentPrice()) + \
                          "\n" + "Balance: " + str(balance) + "$" \
                          "\nDate: " + str(now)

                telegram.send(message)
            if not isinstance(order_sell, dict):
                message = "⛔ " + user.upper() + " non posso vendere, risultano eseerci " + str(
                    round(exchange.getFreePairBalance(),
                          exchange.getSymbolPrecision())) + " " + ticker + " nel tuo account."
                telegram.send(message)

    except Exception as e:
        message = "Error: " + str(e)
        telegram.send(message)

# def threadtradefuturs(value):
#     api_key = value.get('api_key')
#     api_secret = value.get('api_secret')
#     symbol = value.get('symbol')
#     capital = value.get('capital')
#     leverage = value.get('leverage')
#     action = value.get('action')
#     user = value.get('user')
#     telegram = value.get('telegram')
#
#     try:
#
#         exchange = Futures(api_key=api_key,
#                            api_secret=api_secret,
#                            symbol=symbol,
#                            capital=capital,
#                            leverage=leverage)
#
#         # buy
#         if action == 'buy':
#
#             order = exchange.buy()
#             if isinstance(order, Exception):
#                 raise Exception(order)
#
#             if not isinstance(order, Exception):
#                 balance = round(exchange.getBalance(), 3)
#                 current_price = exchange.getCurrentPrice()
#
#                 now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
#                 message = "Buy: " + str(symbol) + " 📈 " + \
#                           "\n" + "User: " + user + \
#                           "\n" + "Market Futures" + \
#                           "\n" + "Buy Price: " + str(current_price) + \
#                           "\n" + "Balance: " + str(balance) + \
#                           "\nDate: " + str(now)
#
#                 telegram.send(message)
#
#         # sell
#         if action == 'sell':
#
#             order = exchange.sell()
#             if isinstance(order, Exception):
#                 raise Exception(order)
#
#             if not isinstance(order, Exception):
#                 balance = round(exchange.getBalance(), 3)
#                 current_price = exchange.getCurrentPrice()
#
#                 now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
#                 message = "Sell: " + str(symbol) + " ✅ " + \
#                           "\n" + "User: " + user + \
#                           "\n" + "Market Futures" + \
#                           "\n" + "Sell Price: " + str(current_price) + \
#                           "\n" + "Balance: " + str(balance) + \
#                           "\nDate: " + str(now)
#
#                 telegram.send(message)
#
#     except Exception as e:
#         message = "Error: " + str(e)
#         telegram.send(message)
