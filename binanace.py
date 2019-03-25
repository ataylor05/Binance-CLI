import numpy
import os
import sys
import configparser
import datetime
from binance.client import Client

os.system('cls')
config = configparser.ConfigParser()
config.read('creds.ini')
selected_profile = config['default']['alias']
client = Client(config[selected_profile]['api_key'], config[selected_profile]['api_secret'])

def os_clear_screen():
    os.system('cls')

def show_connection_info():
    global selected_profile
    global open_orders
    open_orders = client.get_open_orders()
    print("Connected Profile: " + selected_profile)
    if open_orders == "":
        print("No open orders")
    else:
        for open_order in open_orders:
            print("Open Order ID: " + str(open_order['orderId']) + ' - ' + "Symbol: " + open_order['symbol'] + ' - ' + "Price: " + str(open_order['price']) + ' - ' + "Quantity: " + str(open_order['origQty']) + ' - ' + "Executed Quantity: " + str(open_order['executedQty']))

def input_number(prompt):
    while True:
        try:
            number = int(input(prompt))
            break
        except ValueError:
            pass
    return number

def display_menu(menu_items):
    try:
        print("")
        show_connection_info()
        print("")
        for item in range(len(menu_items)):
            print("{:d}. {:s}".format(item + 1, menu_items[item]))
        print("")
        choice = 0
        while not (numpy.any(choice == numpy.arange(len(menu_items))+1)):
            choice = input_number("Choose a menu item: ")
        return choice
    except Exception as e:
        print("")
        print(e.message)

def select_profile(config):
    try:
        global client
        global selected_profile
        profiles = config.sections()
        for item in range(len(profiles)):
            print("{:d}. {:s}".format(item + 1, profiles[item]))
        print("")
        choice = 0
        while not (numpy.any(choice == numpy.arange(len(profiles))+1)):
            choice = input_number("Choose a menu item: ")
        selected_choice = choice - 1
        selected_profile = profiles[selected_choice]
        client = Client(config[selected_profile]['api_key'], config[selected_profile]['api_secret'])
        os_clear_screen()
    except Exception as e:
        print("")
        print(e.message)
    
def show_balances(client):
    try:
        account_info = client.get_account()
        balances = account_info['balances']
        for balance in balances:
            if float(balance['free']) > 0 or float(balance['locked']) > 0:
                print("Asset: " + balance['asset'] + " - " + "Quantity: " + balance['free'] + " - " + "Locked: " + balance['locked'])
    except Exception as e:
        print("")
        print(e.message)

def get_asset_price(client, asset):
    try:
        ticker = client.get_ticker(symbol=asset)
        print("")
        print("Symbol: " + ticker['symbol'] + " - " + "Last Price: " + ticker['lastPrice'] + " - " + "Volume: " + ticker['volume'])
        print("Price Change: " + ticker['priceChange'] + " - " + "Percentage Change: " + ticker['priceChangePercent'] + "%")
        print("Bid Price: " + ticker['bidPrice'] + " - " + "Ask Price: " + ticker['askPrice'])
    except Exception as e:
        print("")
        print(e.message)

def get_asset_details(client, symbol):
    try:
        asset_details = []
        info = client.get_symbol_info(symbol)
        asset_details.append(info["baseAsset"])
        asset_details.append(info["baseAssetPrecision"])
        asset_details.append(info["quoteAsset"])
        asset_details.append(info["quotePrecision"])
        asset_details.append(info["filters"][2]["stepSize"])
        return asset_details
    except Exception as e:
        print("")
        print(e.message)

def buy_order(client, symbol, price):
    try:
        asset_details = get_asset_details(client, symbol)
        base_balance = client.get_asset_balance(asset=asset_details[0])
        quote_balance = client.get_asset_balance(asset=asset_details[2])
        step_size = asset_details[4]
        if float(step_size) == 1.00000000:
            str_to_float = float(quote_balance["free"])
            quantity = float(str_to_float) / float(price)
            quantity_cleaned = int(quantity)
        elif float(step_size) < 1.00000000:
            step_size_split = step_size.split('.')
            step_size_split[1]
            step_size_cleaned = step_size_split[1].rstrip('0')
            step_size_length = len(step_size_cleaned) + 2
            str_to_float = float(quote_balance["free"])
            quantity = float(str_to_float) / float(price)
            back_to_str = str(quantity)
            quantity_cleaned = str(back_to_str[:step_size_length])
        order = client.order_limit_buy(symbol=symbol, quantity=quantity_cleaned, price=price)
        print("")
        print("A " + order['side'] + " order was placed.")
        print("Symbol: " + order['symbol'] + " - " + "OrderId: " + str(order['orderId']) + " - " + "Price: " + str(order['price']) + " - " + "Quantity: " + str(order['origQty']))
    except Exception as e:
        print("")
        print(e.message)

def sell_order(client, symbol, price):
    try:
        asset_details = get_asset_details(client, symbol)
        base_balance = client.get_asset_balance(asset=asset_details[0])
        quote_balance = client.get_asset_balance(asset=asset_details[2])
        step_size = asset_details[4]
        if float(step_size) == 1.00000000:
            str_to_float = float(base_balance["free"])
            quantity = int(str_to_float)
        elif float(step_size) < 1.00000000:
            step_size_split = step_size.split('.')
            step_size_split[1]
            step_size_cleaned = step_size_split[1].rstrip('0')
            step_size_length = len(step_size_cleaned) + 2
            str_to_float = base_balance["free"]
            str_to_float_cleaned = str(str_to_float[:step_size_length])
            quantity =  str(str_to_float[:step_size_length])
        order = client.order_limit_sell(symbol=symbol, quantity=quantity, price=price)
        print("")
        print("A " + order['side'] + " order was placed.")
        print("Symbol: " + order['symbol'] + " - " + "OrderId: " + str(order['orderId']) + " - " + "Price: " + str(order['price']) + " - " + "Quantity: " + str(order['origQty']))
    except Exception as e:
        print("")
        print(e.message)

def cancel_order(client, order_symbol, order_id):
    try:
        cancel = client.cancel_order(symbol=order_symbol, orderId=order_id)
        print("Order Id: " + cancel['orderId'] + " - " + "is " + cancel['status'])
    except Exception as e:
        print("")
        print(e.message)

def get_trades(client, order_symbol):
    try:
        trades = client.get_my_trades(symbol=order_symbol)
        for trade in trades:
            time = trade['time'] / 1000.0
            cleaned_time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M')
            print("Symbol: " + trade['symbol'] + " - " + "OrderId: " + str(trade['orderId']) + " - " + "Price: " + str(trade['price']) + " - " + "Quantity: " + str(trade['qty'])+ " - " + "Time: " + str(cleaned_time))
    except Exception as e:
        print("")
        print(e.message)

menu_items = numpy.array(["Select Profile", \
    "Show Balances Above 0", \
    "Check Asset Price", \
    "Create Buy Order", \
    "Create Sell Order", \
    "Cancel Order", \
    "View Trade History", \
    "Quit"
    ])

choice = display_menu(menu_items)

while True:
    if choice == 1:
        os_clear_screen()
        select_profile(config)
        print("")
        choice = display_menu(menu_items)
    elif choice == 2:
        os_clear_screen()
        show_balances(client)
        print("")
        choice = display_menu(menu_items)
    elif choice == 3:
        os_clear_screen()
        asset = input("Enter an asset pair - ")
        get_asset_price(client, asset.upper())
        print("")
        choice = display_menu(menu_items)
    elif choice == 4:
        os_clear_screen()
        asset = input("Enter an asset pair - ")
        print("")
        price = input("Enter a price to buy at - ")
        buy_order(client, asset.upper(), price)
        print("")
        choice = display_menu(menu_items)
    elif choice == 5:
        os_clear_screen()
        asset = input("Enter an asset pair - ")
        print("")
        price = input("Enter a price to sell at - ")
        sell_order(client, asset.upper(), price)
        print("")
        choice = display_menu(menu_items)
    elif choice == 6:
        asset = input("Enter an asset pair - ")
        print("")
        order_id = input("Enter the Order Id - ")
        cancel_order(client, asset.upper(), order_id)
        print("")
        choice = display_menu(menu_items)
    elif choice == 7:
        os_clear_screen()
        asset = input("Enter an asset pair - ")
        get_trades(client, asset.upper())
        print("")
        choice = display_menu(menu_items)
    elif choice == 8:
        break