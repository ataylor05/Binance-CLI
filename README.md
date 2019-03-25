# Binance-CLI
This project was started as a quick method to interact with Binance while traveling.  It covers a quick and easy method to set orders up from the API without of the GUI overhead.  This tool uses profiles of API credentials so it is easy to trade on multiple accounts.
<br><br>
**Script Screenshot**<br>
![](https://github.com/ataylor05/Binance-CLI/blob/master/files/Binance_CLI.jpg)


## Prerequisites
Python3 along with the module python-binance are required to run this script.  If you are on Windows, you will also need the Visual C++ 14.0 build tools to install python-binance with pip.
<br>
```
pip install python-binance
```
<br>


## Getting Started
Clone project or download the zip file.  Once the Binance-Scalper.py file is on your disk, run it as follows:<br>
```
python .\binanace.py
```
<br><br>
You will also need API keys for the Binanace accounts you want to trade on.  The link below describes the process of creating one.
<br><br>
https://support.binance.com/hc/en-us/articles/360002502072-How-to-create-API


### Creating a creds.ini file
The Binance API creds get defined in a .ini file which is not included in this project so therefore you will need to create one.  Below is an example if what the file should look like.
<br><br>
```python
[default]
alias: default
api_key: 987659123456789123456789123456789123456789
api_secret: 98765789123456789123456789123456789123456789123456789

[profile_name]
alias: profile_name
api_key: 987659123456789123456789123456789123456789
api_secret: 98765789123456789123456789123456789123456789123456789
```
<br><br>
**binance.py - Lines 9 - 12**
```
config = configparser.ConfigParser()
config.read('creds.ini')
selected_profile = config['default']['alias']
client = Client(config[selected_profile]['api_key'], config[selected_profile]['api_secret'])
```

## Disclaimer
** Use this tool at your own risk! I am not resposible for any financial losses as a result of using this script.
<br><br>
Please pay attention to prices when setting up orders!

## Donations
If you find this tool or function patterns useful then donations are always welcome!<br><br>
You can find me on Twitter @Crypto_Watcher_<br><br>

BTC: bc1qvga6sudluhcdru4rg5xyvl7s2ywxtnyffwcwdt<br>
LTC: LKNbQmEqE5k9e9RqfkDsoPzKcFDjPSHyFy

## Acknowledgments
Thanks to sammchardy for writting the Binance API wrappers in Python!<br>
https://github.com/sammchardy/python-binance
