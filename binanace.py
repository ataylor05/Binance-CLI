import numpy
import os
import sys
import time
import platform
import configparser
import datetime
import subprocess
from playsound import playsound
from binance.client import Client

config = configparser.ConfigParser()
config.read('creds.ini')
selected_profile = config['default']['alias']
client = Client(config[selected_profile]['api_key'], config[selected_profile]['api_secret'])

def os_clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def show_connection_info():
    global selected_profile
    global open_orders
    open_orders = client.get_open_orders()
    print("Connected Profile: " + selected_profile)
    if open_orders == "":
        print("No open orders")
    else:
        for open_order in open_orders:
            cleaned_quantity = ("%.2f" % float(open_order['origQty']))
            cleaned_exe_quantity = ("%.2f" % float(open_order['executedQty']))
            print("Open Order ID: " + str(open_order['orderId']) + ' - ' + "Symbol: " + open_order['symbol'] + ' - ' + "Price: " + str(open_order['price']) + ' - ' + "Quantity: " + str(cleaned_quantity) + ' - ' + "Executed Quantity: " + str(cleaned_exe_quantity))

def input_number(prompt):
    while True:
        try:
            number = int(input(prompt))
            break
        except ValueError:
            pass
    return number

def display_menu():
    try:
        menu_items = numpy.array(["Select Profile", \
            "Show Balances Above 0", \
            "Check Asset Price", \
            "Create Buy Order", \
            "Create Sell Order", \
            "Cancel Order", \
            "View Trade History", \
            "Watch Opened Order", \
            "Quit"
        ])
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

def order_type_menu():
    try:
        print("")
        order_types = numpy.array(["LIMIT", \
            "MARKET", \
            "STOP-LOSS", \
            "Cancel and go back"
        ])
        for item in range(len(order_types)):
            print("{:d}. {:s}".format(item + 1, order_types[item]))
        print("")
        choice = 0
        while not (numpy.any(choice == numpy.arange(len(order_types))+1)):
            choice = input_number("Choose a menu item: ")
        return choice
    except Exception as e:
        print("")
        print(e.message)

def buy_order(client):
    choice = order_type_menu()
    while True:
        if choice == 1:
            print("")
            symbol = input("Enter an asset pair - ")
            print("")
            price = input("Enter a price to buy at - ")
            buy_limit_order(client, symbol.upper(), price)
            break
        elif choice == 2:
            print("")
            symbol = input("Enter an asset pair - ")
            print("Market")
            break
        elif choice == 3:
            print("")
            symbol = input("Enter an asset pair - ")
            print("")
            stop_price = input("Enter a stop price - ")
            print("")
            limit_price = input("Enter a limit price above the stop price - ")
            print("Stop")
            break
        elif choice == 4:
            break

def buy_limit_order(client, symbol, price):
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
        os_clear_screen()
        print("A " + order['side'] + " order was placed.")
        print("Symbol: " + order['symbol'] + " - " + "OrderId: " + str(order['orderId']) + " - " + "Price: " + str(order['price']) + " - " + "Quantity: " + str(order['origQty']))
    except Exception as e:
        print("")
        print(e.message)

def sell_order(client):
    choice = order_type_menu()
    while True:
        if choice == 1:
            print("")
            symbol = input("Enter an asset pair - ")
            print("")
            price = input("Enter a price to sell at - ")
            sell_limit_order(client, symbol.upper(), price)
            break
        elif choice == 2:
            print("")
            symbol = input("Enter an asset pair - ")
            print("Market")
            break
        elif choice == 3:
            print("")
            symbol = input("Enter an asset pair - ")
            print("")
            stop_price = input("Enter a stop price - ")
            print("")
            limit_price = input("Enter a limit price above the stop price - ")
            print("Stop")
            break
        elif choice == 4:
            break

def sell_limit_order(client, symbol, price):
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
        os_clear_screen()
        print("")
        print("A " + order['side'] + " order was placed.")
        print("Symbol: " + order['symbol'] + " - " + "OrderId: " + str(order['orderId']) + " - " + "Price: " + str(order['price']) + " - " + "Quantity: " + str(order['origQty']))
    except Exception as e:
        print("")
        print(e.message)

def cancel_order(client, order_symbol, order_id):
    try:
        cancel = client.cancel_order(symbol=order_symbol, orderId=order_id)
        print("Order Id: " + str(cancel['orderId']) + " - " + "is " + cancel['status'])
    except Exception as e:
        print("")
        print(e.message)

def get_trades(client, order_symbol):
    try:
        trades = client.get_my_trades(symbol=order_symbol)
        for trade in trades:
            time = trade['time'] / 1000.0
            cleaned_quantity = ("%.2f" % float(trade['qty']))
            cleaned_time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M')
            print("Symbol: " + trade['symbol'] + " - " + "OrderId: " + str(trade['orderId']) + " - " + "Price: " + str(trade['price']) + " - " + "Quantity: " + str(cleaned_quantity)+ " - " + "Time: " + str(cleaned_time))
    except Exception as e:
        print("")
        print(e.message)

def watch_open_order(client, symbol, order_id):
    while True:
        os_clear_screen()
        try:
            order_status = client.get_order(symbol=symbol, orderId=order_id)
            cleaned_quantity = ("%.2f" % float(order_status["origQty"]))
            cleaned_exe_quantity = ("%.2f" % float(order_status["executedQty"]))
            print("Order Id: " + str(order_status["orderId"]) + " is " + order_status["status"])
            print("Order Type: " + order_status["type"] + "-" + order_status["side"])
            print(str(cleaned_exe_quantity) + " Executed out of " + str(cleaned_quantity))
            print("")
            print("Press Ctrl + c to return to menu.")
            if order_status["status"] == "FILLED" or order_status["status"] == "CANCELED":
                playsound('files/alert.mp3')
                break
            time.sleep(60)
        except Exception as e:
            print("")
            print(e.message)

os_clear_screen()
choice = display_menu()

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
        buy_order(client)
        print("")
        choice = display_menu()
    elif choice == 5:
        os_clear_screen()
        sell_order(client)
        print("")
        choice = display_menu()
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
        symbol = input("Enter an asset pair - ")
        print("")
        order_id = input("Enter an opened Order Id - ")
        watch_open_order(client, symbol.upper(), order_id)
        print("")
        choice = display_menu(menu_items)
    elif choice == 9:
        break