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
                          "\n" + "Balance: " + str(balance) + " " + asset + \
                          "\nDate: " + str(now)

                telegram.send(message)

            # Se l'ordine non è un dizionario allora non è stato creato
            if isinstance(order_buy, Exception):
                message = "⛔ " + user.upper() + " non posso comprare, risultano eseerci " + str(
                    round(exchange.getFreeAssetBalance(),
                          2)) + " " + asset + " nel tuo account è necessaria una quantità maggiore di 10." + " errore " + str(order_buy)
                telegram.send(message)

        # sell
        if action == 'sell':

            order_sell = exchange.sell()
            app.log.debug("Order sell: " + str(order_sell))

            if isinstance(order_sell, dict):

                balance = round(exchange.getFreeAssetBalance(), 3)
                executedQty = float(order_sell.get('executedQty'))

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

                message = "Sell Spot: " + str(ticker) + " ✅ " + \
                          "\n" + "User: " + user + \
                          "\n" + "Market Spot" \
                          "\n" + "Sell Price: " + str(exchange.getCurrentPrice()) + "$" \
                          "\n" + "Quantity: " + str(round(executedQty, exchange.getSymbolPrecision())) + \
                          "\n" + "Balance: " + str(round(balance, 2)) + " " + asset +\
                          "\nDate: " + str(now)

                telegram.send(message)

            if isinstance(order_sell, Exception):
                message = "⛔ " + user.upper() + " non posso vendere, risultano eseerci " + str(
                    round(exchange.getFreePairBalance(),
                          exchange.getSymbolPrecision())) + " " + ticker + " nel tuo account, che sono inferiori a 10$" + " errore " + str(order_sell)
                telegram.send(message)

    except Exception as e:
        message = "Error: " + str(e)
        telegram.send(message)
