from threading import Thread
from chalice import Chalice
from chalicelib.telegram import Telegram
from chalicelib.trade import tradespot

app = Chalice(app_name='bot')
app.debug = True


@app.route("/")
def index():
    return {"Hello": "Traders"}

@app.route('/tradingbotpriceaction', methods=['POST'])
def tradingbotpriceaction():

    """
    JSON body
    {
        "action": "{{strategy.order.action}}",
        "exchange": "{{exchange}}",
        "ticker": "{{ticker}}",
        "asset": "BUSD" / or "USDT"
        "coins": {{ number of coins }} // for division balance
    }
    """

    users = {

        'test': {
            'key': '',
            'secret': '',
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

        'test': {
            'key': '',
            'secret': '',
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
