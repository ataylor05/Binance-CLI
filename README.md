# Binance-CLI
This project is a quick method to interact with multiple Binance accounts.  The general goal of the project is to execute an action once and the action gets executed on multiple accounts.  This will require API credentails from Binance.


## Prerequisites
Use the requirements.txt file to install Python dependencies.<br>
<pre>
cd Binance-CLI
pip install -r requirements.txt
</pre>


## Getting Started
Get command help.<br>
<pre>
python binanace-cli.py -h
</pre>


### Creating profile creds
Create an API profile
<pre>
python binanace-cli.py --add testProfile 12345678901234567890 abcdefghijklmnopqrstuvwxyz
</pre><br><br>

View saved API profiles
<pre>
python binanace-cli.py --profiles
</pre>


## Commands
Shows balances for all profiles.<br>
<pre>
python binanace-cli.py --balance
</pre><br><br>

Gets ticker info on a symbol.<br>
<pre>
python binanace-cli.py --ticker btcusdt
</pre><br><br>

Gets details on a symbol.<br>
<pre>
python binanace-cli.py --symbol btcusdt
</pre><br><br>

Opens a limit order trade.  The app is intended to execute trades on multiple Binance profiles, therefore trades need to specified in percentages.<br>
<pre>
python binanace-cli.py --open <symbol> <side> <price> <percentage>
python binanace-cli.py --open btcusdt  buy    17000   10
</pre><br><br>

Gets open orders on a symbol for all profiles.<br>
<pre>
python binanace-cli.py --get btcusdt
</pre><br><br>

Cancels all open orders on a symbol for all profiles.<br>
<pre>
python binanace-cli.py --cancel btcusdt
</pre><br><br>

Views all open orders on a symbol for all profiles.<br>
<pre>
python binanace-cli.py --view btcusdt
</pre><br><br>

## Disclaimer
** Use this tool at your own risk! I am not resposible for any financial losses as a result of using this program.
<br><br>
**Please pay attention to prices when setting up orders!**