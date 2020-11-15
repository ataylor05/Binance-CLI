import os
import logging
import datetime
from binance.client import Client

class Bclient():

    def __init__(self, apiKey, apiSecret):
        self.client = Client(apiKey, apiSecret)

    def showBalances(self):
        try:
            accountInfo = self.client.get_account()
            balances = accountInfo['balances']
            for balance in balances:
                if float(balance['free']) > 0 or float(balance['locked']) > 0:
                    print(balance['asset'] + " - " + "Quantity: " + balance['free'] + " - " + "Locked: " + balance['locked'])
        except Exception as e:
            logging.error(e)

    def showAssetBalance(self, asset):
        try:
            accountInfo = self.client.get_asset_balance(asset=asset)
            return accountInfo['free']
        except Exception as e:
            logging.error(e)

    def getTicker(self, symbol):
        try:
            ticker = self.client.get_ticker(symbol=symbol)
            print("")
            print(ticker['symbol'] + " - " + "Last Price: " + ticker['lastPrice'] + " - " + "Volume: " + ticker['volume'])
            print("Price Change: " + ticker['priceChange'] + " - " + "Percentage Change: " + ticker['priceChangePercent'] + "%")
            print("Bid Price: " + ticker['bidPrice'] + " - " + "Ask Price: " + ticker['askPrice'])
            print("")
        except Exception as e:
            logging.error(e)

    def getSymbolDetails(self, symbol):
        try:
            info = self.client.get_symbol_info(symbol)
            assetDetails = []
            assetDetails.append(info["baseAsset"])
            assetDetails.append(info["baseAssetPrecision"])
            assetDetails.append(info["quoteAsset"])
            assetDetails.append(info["quotePrecision"])
            assetDetails.append(info["filters"][2]["stepSize"])
            return assetDetails
        except Exception as e:
            logging.error(e)

    def getOrderVolume(self, assetAmount, percentage):
        try:
            percentageDecimal = float(percentage) / 100.0
            return (float(assetAmount) / percentageDecimal) / 100
        except Exception as e:
            logging.error(e)

    def getOrderPrecision(self, assetVolume, precision):
        try:
            precision = precision.rstrip("0")
            decimals = str(precision[::-1].find('.'))
            strAssetVolume = str(assetVolume)
            volumeBeforeSplit = strAssetVolume.split(".")
            volumeBeforeDecimal = str(volumeBeforeSplit[0])
            volumeAfterDecimal = str(volumeBeforeSplit[1])
            afterDecimalPrecision = volumeAfterDecimal[:int(decimals)]
            return str(volumeBeforeDecimal) + "." + str(afterDecimalPrecision)
        except Exception as e:
            logging.error(e)

    def createBuyLimitOrder(self, symbol, price, percentage):
        try:
            symbolDetails = self.getSymbolDetails(symbol)
            stepSize = symbolDetails[4]
            quoteBalance = self.showAssetBalance(asset=symbolDetails[2])
            volumeSize = self.getOrderVolume(quoteBalance, percentage)
            preciseVolumeSize = self.getOrderPrecision(volumeSize, stepSize)
            print("Quote Balance: " + quoteBalance)
            print("Quote Volume: " + str(preciseVolumeSize))
            print(self.client.order_limit_buy(symbol=symbol, quantity=str(preciseVolumeSize), price=str(price)))
        except Exception as e:
            logging.error(e)

    def createSellLimitOrder(self, symbol, price, percentage):
        try:
            symbolDetails = self.getSymbolDetails(symbol)
            stepSize = symbolDetails[4]
            baseBalance = self.showAssetBalance(asset=symbolDetails[0])
            volumeSize = self.getOrderVolume(baseBalance, percentage)
            preciseVolumeSize = self.getOrderPrecision(volumeSize, stepSize)
            print("Base Balance: " + baseBalance)
            print("Base Volume: " + str(preciseVolumeSize))
            self.client.order_limit_sell(symbol=symbol, quantity=str(preciseVolumeSize), price=str(price))
        except Exception as e:
            logging.error(e)

    def getOpenOrders(self, symbol):
        try:
            orders = self.client.get_open_orders(symbol=symbol)
            orderList = []
            for order in orders:
                time = order['time'] / 1000.0
                cleaned_quantity = ("%.2f" % float(order['origQty']))
                cleaned_time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M')
                orderList.append(order['orderId'])
                print("OrderId: " + str(order['orderId']) + " -  Price: " + str(order['price']) + " -  Quantity: " + str(cleaned_quantity)+ " -  Time: " + str(cleaned_time) + "  -  Executed Qty: " + order['executedQty'])
            return orderList
        except Exception as e:
            logging.error(e)

    def cancelAllOpenOrders(self, symbol):
        try:
            orders = self.getOpenOrders(symbol)
            for order in orders:
                cancel = self.client.cancel_order(symbol=symbol, orderId=order)
                print("Order Id: " + str(cancel['orderId']) + " - " + "is " + cancel['status'])
        except Exception as e:
            logging.error(e)
