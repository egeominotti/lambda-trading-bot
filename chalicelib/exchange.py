import math

import requests
from binance import Client
from binance.enums import *
from chalice import Chalice

app = Chalice(app_name='bot')


class Spot:

    def __init__(
            self,
            api_key,
            api_secret,
            symbol,
            quantity,
    ):
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.symbol = symbol
        self.quantity = quantity

    def getSymbolPrecision(self):

        symbol_info = self.client.get_symbol_info(self.symbol)
        step_size = 0.0
        for f in symbol_info['filters']:
            if f['filterType'] == 'LOT_SIZE':
                step_size = float(f['stepSize'])
                print(step_size)
        precision = int(round(-math.log(step_size, 10), 0))
        return precision

    def getBalance(self):
        balances = self.client.get_account()
        for _balance in balances["balances"]:
            if _balance["asset"] == 'BUSD':
                usdt = _balance["free"]
                return float(usdt)

    def getCurrentPrice(self):
        return float(self.client.get_symbol_ticker(symbol=self.symbol)['price'])

    def buyAmount(self):

        max_buy = 0

        # usa tutto il capitale
        if self.quantity == 0:
            balance_buy = float(self.client.get_asset_balance(asset='BUSD')['free'])
            close = float(self.client.get_symbol_ticker(symbol=self.symbol)['price'])
            max_buy = round(balance_buy / close * .997, self.getSymbolPrecision())

        if self.quantity > 0:
            close = float(self.client.get_symbol_ticker(symbol=self.symbol)['price'])
            max_buy = round(self.quantity / close, self.getSymbolPrecision())

        return max_buy

    def sellAmount(self):

        max_sell = 0

        if self.quantity > 0:
            max_sell = round(self.quantity * .997, self.getSymbolPrecision())

        if self.quantity == 0:
            balance_sell = float(self.client.get_asset_balance(asset=self.symbol.replace('BUSD', ''))['free'])
            max_sell = round(balance_sell * .997, self.getSymbolPrecision())

        return max_sell

    def sell(self):

        return self.client.create_order(
            symbol=self.symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=self.sellAmount(),
        )

    def buy(self):

        return self.client.create_order(
            symbol=self.symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=self.buyAmount(),
        )


class Futures:

    def __init__(
            self,
            api_key,
            api_secret,
            symbol,
            capital,
            leverage
    ):
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.symbol = symbol
        self.leverage = leverage
        self.capital = capital
        self.client.futures_change_leverage(symbol=symbol, marginType='ISOLATED', leverage=leverage)

    def getQuantity(self):

        current_balance = self.getBalance() * self.capital
        symbol_precision = self.getSymbolPrecision()
        current_price = self.getCurrentPrice()

        total = (current_balance / current_price) * self.leverage
        quantity = round(total, symbol_precision)

        return quantity

    def getSymbolPrecision(self):
        symbols_n_precision = {}
        info = self.client.futures_exchange_info()
        for item in info['symbols']:
            symbols_n_precision[item['symbol']] = item['quantityPrecision']

        return symbols_n_precision[self.symbol]

    def getCurrentPrice(self):
        resp = requests.get('https://fapi.binance.com/fapi/v1/ticker/price?symbol=' + self.symbol).json()
        price = float(resp['price'])
        return price

    def getBalance(self, coin='USDT'):

        item = {}
        account_balance = self.client.futures_account_balance()

        for k in account_balance:
            item[k['asset']] = k['balance']
        if coin is not None:
            return float(item[coin])
        return item

    def getOriginalQty(self):

        current_order = self.client.futures_get_all_orders(symbol=self.symbol, limit=1)

        order_id = current_order[0]['orderId']
        status = current_order[0]['status']
        avg_price = current_order[0]['avgPrice']
        orig_qty = current_order[0]['origQty']
        cum_quote = current_order[0]['cumQuote']

        return float(orig_qty)

    def sell(self):

        try:

            quantity = self.getOriginalQty()

            if quantity > 0:
                order = self.client.futures_create_order(
                    symbol=self.symbol,
                    side=SIDE_SELL,
                    type=ORDER_TYPE_MARKET,
                    quantity=self.getOriginalQty(),
                )

                return order

            return Exception("quantity must be greater than 0")


        except Exception as e:
            print(str(e))
            return e

    def buy(self):

        try:

            quantity = self.getQuantity()

            if quantity > 0:
                order = self.client.futures_create_order(
                    symbol=self.symbol,
                    side=SIDE_BUY,
                    type=ORDER_TYPE_MARKET,
                    quantity=self.getQuantity(),
                )

                return order

            return Exception("quantity must be greater than 0")

        except Exception as e:
            print(str(e))
            return e

    def close_order(self):
        self.client.futures_cancel_all_open_orders(symbol=self.symbol)
