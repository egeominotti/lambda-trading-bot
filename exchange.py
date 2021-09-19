import math
from binance import Client
from binance.enums import *


class SpotExchange:

    def __init__(
            self,
            api_key,
            api_secret,
            symbol,
    ):
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.symbol = symbol

    def get_symbol_precision(self):

        symbol_info = self.client.get_symbol_info(self.symbol)
        step_size = 0.0
        for f in symbol_info['filters']:
            if f['filterType'] == 'LOT_SIZE':
                step_size = float(f['stepSize'])
                print(step_size)
        precision = int(round(-math.log(step_size, 10), 0))
        return precision

    def spot_usdt_balance(self):
        balances = self.client.get_account()
        for _balance in balances["balances"]:
            if _balance["asset"] == 'USDT':
                usdt = _balance["free"]
                return float(usdt)

    def buyAmount(self):

        balance_buy = float(self.client.get_asset_balance(asset='USDT')['free'])
        close = float(self.client.get_symbol_ticker(symbol=self.symbol)['price'])
        max_buy = round(balance_buy / close * .995, self.get_symbol_precision())

        return max_buy

    def sellAmount(self):

        balance_sell = float(self.client.get_asset_balance(asset=self.symbol.replace('USDT', ''))['free'])
        max_sell = round(balance_sell * .995, self.get_symbol_precision())
        return max_sell

    def sell(self):

        quantity = self.sellAmount()
        return self.client.create_order(
            symbol=self.symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity,
        )

    def buy(self):

        quantity = self.buyAmount()
        return self.client.create_order(
            symbol=self.symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity,
        )
