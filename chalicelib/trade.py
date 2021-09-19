import sys

from chalicelib.exchange import Futures
import datetime


def threadtradefuturs(value):
    api_key = value.get('api_key')
    api_secret = value.get('api_secret')
    symbol = value.get('symbol')
    capital = value.get('capital')
    leverage = value.get('leverage')
    action = value.get('action')
    user = value.get('user')
    telegram = value.get('telegram')

    try:

        exchange = Futures(api_key=api_key,
                           api_secret=api_secret,
                           symbol=symbol,
                           capital=capital,
                           leverage=leverage)

        # buy
        if action == 'buy':

            order = exchange.buy()
            if isinstance(order, Exception):
                raise Exception(order)

            if not isinstance(order, Exception):
                balance = round(exchange.getBalance(), 3)
                current_price = exchange.getCurrentPrice()

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                message = "Buy: " + str(symbol) + " 📈 " + \
                          "\n" + "User: " + user + \
                          "\n" + "Market Futures" + \
                          "\n" + "Buy Price: " + str(current_price) + \
                          "\n" + "Balance: " + str(balance) + \
                          "\nDate: " + str(now)

                telegram.send(message)

        # sell
        if action == 'sell':

            order = exchange.sell()
            if isinstance(order, Exception):
                raise Exception(order)

            if not isinstance(order, Exception):
                balance = round(exchange.getBalance(), 3)
                current_price = exchange.getCurrentPrice()

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                message = "Sell: " + str(symbol) + " ✅ " + \
                          "\n" + "User: " + user + \
                          "\n" + "Market Futures" + \
                          "\n" + "Sell Price: " + str(current_price) + \
                          "\n" + "Balance: " + str(balance) + \
                          "\nDate: " + str(now)

                telegram.send(message)

    except Exception as e:
        message = "Error: " + str(e)
        telegram.send(message)
