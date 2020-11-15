import os
import sys
import configparser
import argparse
import datetime
from bclient import Bclient

global profilesFile
profilesFile = "profiles.ini"

parser = argparse.ArgumentParser(description="Binance CLI")
parser.add_argument("-p", "--profiles", action="store_true", help="Shows stored profiles")
parser.add_argument("-a", "--add", nargs=3, help="Add a profile, requires <name> <apiKey> <apiSecret>")
parser.add_argument("-b", "--balance", action="store_true", help="Shows asset balances")
parser.add_argument("-t", "--ticker", nargs=1, help="Gets ticker info on a symbol, requires <symbol>")
parser.add_argument("-s", "--symbol", nargs=1, help="Gets details on a symbol, requires <symbol>")
parser.add_argument("-o", "--open", nargs=4, help="Opens a limit order trade, requires <symbol> <side> <price> <percentage>")
parser.add_argument("-g", "--get", nargs=1, help="Gets open orders, requires <symbol>")
parser.add_argument("-c", "--cancel", nargs=1, help="Cancels all open orders on a symbol, requires <symbol>")
parser.add_argument("-v", "--view", nargs=1, help="Views all open orders on a symbol, requires <symbol>")
args = parser.parse_args()

def readProfiles(config):
    for section_name in config.sections():
        print(section_name)
        for name, value in config.items(section_name):
            print("  %s %s" % (name, value))
        print(" ")

def addCredential(config, name, apiKey, apiSecret):
    config.read(profilesFile)
    config.add_section("binance_" + name)
    config.set("binance_" + name, 'apiKey', apiKey)
    config.set("binance_" + name, 'apiSecret', apiSecret)
    cfgfile = open(profilesFile,'w')
    config.write(cfgfile)
    cfgfile.close()

def main():
    if not os.path.exists(profilesFile):
        with open(profilesFile, 'w') as fp: 
            pass
    config = configparser.ConfigParser()
    config.read(profilesFile)
    
    clients= []
    for section in config.sections():
        bclient = Bclient(config.items(section)[0][1], config.items(section)[1][1])
        clients.append(bclient)

    if args.profiles:
        readProfiles(config)

    if args.add:
        addCredential(config, args.add[0], args.add[1], args.add[2])

    if args.balance:
        for client in clients:
            client.showBalances()
            print("")

    if args.ticker:
        clients[0].getTicker(args.ticker[0].upper())

    if args.symbol:
        clients[0].getSymbolDetails(args.symbol[0].upper())

    if args.open:
        for client in clients:
            if args.open[1] =="buy":
               client.createBuyLimitOrder(args.open[0].upper(), args.open[2], args.open[3])
            elif args.open[1] =="sell":
               client.createSellLimitOrder(args.open[0].upper(), args.open[2], args.open[3])
            print("")

    if args.get:
        for client in clients:
            client.getOpenOrders(args.get[0].upper())
            print("")

    if args.cancel:
        for client in clients:
            client.cancelAllOpenOrders(args.cancel[0].upper())
            print("")

if __name__ == '__main__':
    main()


