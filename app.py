from threading import Thread
from chalice import Chalice
from chalicelib.telegram import Telegram
from chalicelib.trade import tradespot

app = Chalice(app_name='bot')
app.debug = True


@app.route("/")
def index():
    return {"Hello": "Traders"}


@app.route('/tradingspot', methods=['POST'])
def tradingspot():

    """
    JSON body
    {
        "action": "{{strategy.order.action}}",
        "exchange": "{{exchange}}",
        "ticker": "{{ticker}}",
        "asset": "BUSD" / or "USDT"
    }
    """

    users = {

        'egeo': {
            'key': 'g4m5LHCwMI1evVuaf6zgKXtszDnSboQla5O5c7uWVtBmdbaiTLNQWPnO9ImbYB9U',
            'secret': 'b2kxHirJLXDrXuFGvLWUtXvRyUXQu4NvsY8lSy94bJjnJFn0SmESuBq60DJi9b0B',
        },
        'carlo': {
            'key': 'skorPuUbg9lMP15I2WAcjTwKH84o0mDg6iTCLFxWti2bWtBOOgDET3XlkFh2oiJB',
            'secret': 'GA57mual3HxhqsaLI7HUJd5UQtWUMaFUtxSVIoECfHNKKNXprKYGrNf8NhX2LXa2',
        },
        'matteo': {
            'key': 'HgXwZ71GumHVtSDXLEApPA1khbjzFP5PitUjDFX4YWD60TOC5764gRhWgst6BclC',
            'secret': 'aeF2oUUROf4V0cxr0wOORKtZachDukTkUTC0zuXmnMJuUZBuqVcYGZWF6g1RsfEK',
        },
        'giuseppe': {
            'key': 'cGAkMTuEYViqLzQ1jqlRG6RnOnZgSCbdh5gCwgPLvKABjbfnZimN5HKNEf9TSp6T',
            'secret': 'CROpCy26Koy6ufPcgx4C59dhHeMKbGXWiM4DccsFijcdPnkItH93PlNJAlUP1DJ5',
        },
    }

    request = app.current_request
    data = request.json_body

    action = data.get('action')
    ticker = data.get('ticker')
    asset = data.get('asset')

    telegram = Telegram()

    thread_list = list()
    for k, v in users.items():
        app.log.debug("User: " + str(k))

        api_key = v.get('key')
        api_secret = v.get('secret')

        values = {
            'api_key': api_key,
            'api_secret': api_secret,
            'action': action,
            'ticker': ticker,
            'telegram': telegram,
            "asset": asset,
            'user': k
        }

        thread = Thread(target=tradespot, args=(values,))
        thread.daemon = True
        app.log.debug("Thread for: " + str(k))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    return {'Trade': True}
