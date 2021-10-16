import datetime
from threading import Thread
from chalice import Chalice
from chalicelib.telegram import Telegram
from chalicelib.exchange import Spot
from chalicelib.trade import threadtradefuturs

app = Chalice(app_name='bot')
app.debug = True


@app.route("/")
def index():
    return {"Hello": "Traders"}


@app.route('/tradingspot', methods=['POST'])
def tradingspot():
    """
    JSON

    {
        "action": "{{strategy.order.action}}",
        "exchange": "{{exchange}}",
        "ticker": "{{ticker}}",
    }

    """

    users = {

        'egeo': {
            'key': 'vyghMLzH2Pvr0TCoV11Equ9kIK2jxL6ZpDh8pyUBz4hvAWXSLWO6rBHbogQmX9lH',
            'secret': 'yTmr8uu0w3ARIzTlYadGkWX79BlTHSybzzJeInrWcjUoygP3K7t81j4WXd8amMOM',
            'quantity': 0,
        },
        'carlo': {
            'key': 'skorPuUbg9lMP15I2WAcjTwKH84o0mDg6iTCLFxWti2bWtBOOgDET3XlkFh2oiJB',
            'secret': 'GA57mual3HxhqsaLI7HUJd5UQtWUMaFUtxSVIoECfHNKKNXprKYGrNf8NhX2LXa2',
            'quantity': 0,
        },
        'matteo': {
            'key': 'HgXwZ71GumHVtSDXLEApPA1khbjzFP5PitUjDFX4YWD60TOC5764gRhWgst6BclC',
            'secret': 'aeF2oUUROf4V0cxr0wOORKtZachDukTkUTC0zuXmnMJuUZBuqVcYGZWF6g1RsfEK',
            'quantity': 0,
        },
        'giuseppe': {
            'key': 'cGAkMTuEYViqLzQ1jqlRG6RnOnZgSCbdh5gCwgPLvKABjbfnZimN5HKNEf9TSp6T',
            'secret': 'CROpCy26Koy6ufPcgx4C59dhHeMKbGXWiM4DccsFijcdPnkItH93PlNJAlUP1DJ5',
            'quantity': 0,
        },
    }

    request = app.current_request
    data = request.json_body

    action = data.get('action')
    ticker = data.get('ticker')

    telegram = Telegram()

    for k, v in users.items():

        try:
            exchange = Spot(api_key=v.get('key'), api_secret=v.get('secret'), symbol=ticker, quantity=v.get('quantity'))

            # buy
            if action == 'buy':
                # Buy asset with quantity
                order = exchange.buy()
                # Fetch balance
                balance = round(exchange.getBalance(), 3)

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                message = "Buy Spot: " + str(ticker) + " 📈 " + \
                          "\n" + "User: " + k + \
                          "\n" + "Market Spot" \
                          "\n" + "Buy Price: " + str(exchange.getCurrentPrice()) + \
                          "\n" + "Balance: " + str(balance) + "$" \
                          "\nDate: " + str(now)

                telegram.send(message)

            # sell
            if action == 'sell':

                order = exchange.sell()
                balance = round(exchange.getBalance(), 3)

                now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                message = "Sell Spot: " + str(ticker) + " ✅ " + \
                          "\n" + "User: " + k + \
                          "\n" + "Market Spot" \
                          "\n" + "Sell Price: " + str(exchange.getCurrentPrice()) + \
                          "\n" + "Balance: " + str(balance) + "$" \
                          "\nDate: " + str(now)

                telegram.send(message)

        except Exception as e:
            message = "Error: " + str(e)
            telegram.send(message)

    return {'Trade': True}

# @app.route('/tradingfutures', methods=['POST'])
# def tradingfutures():
#     """
#     JSON
#
#     {
#         "action": "{{strategy.order.action}}",
#         "exchange": "{{exchange}}",
#         "ticker": "{{ticker}}",
#         "leverage": 3,
#         "capital": 0.30
#     }
#     """
#
#     users = {
#         'egeo': {
#             'key': 'vyghMLzH2Pvr0TCoV11Equ9kIK2jxL6ZpDh8pyUBz4hvAWXSLWO6rBHbogQmX9lH',
#             'secret': 'yTmr8uu0w3ARIzTlYadGkWX79BlTHSybzzJeInrWcjUoygP3K7t81j4WXd8amMOM'
#         },
#         'carlo': {
#             'key': 'skorPuUbg9lMP15I2WAcjTwKH84o0mDg6iTCLFxWti2bWtBOOgDET3XlkFh2oiJB',
#             'secret': 'GA57mual3HxhqsaLI7HUJd5UQtWUMaFUtxSVIoECfHNKKNXprKYGrNf8NhX2LXa2'
#         },
#     }
#
#     combination = {
#         "ETHUSDTPERP": "ETHUSDT",
#         "BTCUSDTPERP": "BTCUSDT"
#     }
#
#     request = app.current_request
#     data = request.json_body
#
#     action = data.get('action')
#     symbol = combination[data.get('ticker')]
#     leverage = data.get('leverage')
#     capital = data.get('capital')
#
#     telegram = Telegram()
#
#     thread_list = list()
#     for k, v in users.items():
#         api_key = v.get('key')
#         api_secret = v.get('secret')
#
#         values = {
#             'api_key': api_key,
#             'api_secret': api_secret,
#             'action': action,
#             'symbol': symbol,
#             'capital': capital,
#             'leverage': leverage,
#             'telegram': telegram,
#             'user': k
#         }
#
#         thread = Thread(target=threadtradefuturs, args=(values,))
#         # thread.daemon = True
#         app.log.debug("Thread for: " + str(k))
#         thread_list.append(thread)
#         thread.start()
#
#     for thread in thread_list:
#         thread.join()
#
#     return {'Trade': True}
