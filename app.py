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
            'key': 'qElsCKJ7X6Dk8W7WmC5ww3z5nYl3mrAGHGhq1TtG3pOlje6cE0tX2bjSpwrWbJwC',
            'secret': 'Vyx1jqaKWHv4SWr7aoRoalVIkaDQXh8pg5E9bi3lPDLh9p7tieHfCDvQaFKcsKJj',
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
