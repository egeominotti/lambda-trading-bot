import math
import requests
from binance import Client
from binance.enums import *
from chalice import Chalice

app = Chalice(app_name='bot')
app.debug = True


class Spot:

    def __init__(
            self,
            api_key,
            api_secret,
            symbol,
            asset,
    ):
        self.client = Client(api_key=api_key, api_secret=api_secret)
        self.symbol = symbol
        self.asset = asset

    def getSymbolPrecision(self):

        symbol_info = self.client.get_symbol_info(self.symbol)
        step_size = 0.0
        for f in symbol_info['filters']:
            if f['filterType'] == 'LOT_SIZE':
                step_size = float(f['stepSize'])
        precision = int(round(-math.log(step_size, 10), 0))
        return precision

    def getBalance(self):
        balances = self.client.get_account()
        for _balance in balances["balances"]:
            if _balance["asset"] == self.asset:
                free_asset = _balance["free"]
                return float(free_asset)

    def getCurrentPrice(self):
        return float(self.client.get_symbol_ticker(symbol=self.symbol)['price'])

    def getFreeAssetBalance(self):
        return float(self.client.get_asset_balance(asset=self.asset)['free'])

    def getFreePairBalance(self):
        return float(self.client.get_asset_balance(asset=self.symbol.replace(self.asset, ''))['free'])

    def buyAmount(self):

        max_buy = round(self.getFreeAssetBalance() / self.getCurrentPrice() * .998, self.getSymbolPrecision())
        app.log.debug("Max buy: " + str(max_buy))
        return max_buy

    def sellAmount(self):
        max_sell = round(self.getFreePairBalance() * .998, self.getSymbolPrecision())
        app.log.debug("Max sell: " + str(max_sell))

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
