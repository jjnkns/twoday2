# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 12:44:34 2018

@author: jjnkn
"""

#Build a trading application that can scrape quotes from finance.yahoo.com
#The user can buy, sell, view trades and view current cash balance
#Store the trade information on a custom blockchain (i.e. 10 trades per block)
#Store a real-time profit / loss for each stock using dictionaries and VWAP algorithm
#VWAP = volume-weighted average price
#price multiplied by number of shares traded) and then dividing by the total shares traded for the day.
#Read up on Python pickling and find a mechanism to store the blockchain to disk
#and retrieve it even after the app is stopped and restarts. Feel free to use JSON format.'''




#from http://empirica.io/blog/vwap-algorithm/
#typical price = close + high + low divided by 3
#or open + close + high + low divided by 4


'''First, only if we use intraday data for examination, 
we need to calculate typical price for our intervals. 
Then multiply the price by period’s volume and create 
running total of these values for future trades. 
Fourthly we create cumulative volume and in the end we 
divide cumulative multiplication of price and volume by 
running total of volume to obtain VWAP. 
Even simpler, VWAP is a turnover divided by total volume.'''

#from lxml import html
import requests
import json
#import argparse
import datetime as dt

import urllib3
from bs4 import BeautifulSoup
http = urllib3.PoolManager()

#import csv



import pandas as pd


action_menu = {1:'Buy',2:'Sell',3:'View Balance',4:'Exit'}

#initialize booleans for trade sides
BUY = True
SELL = False


class Trade:
    def __init__(self, quantity, price, symbol):
        self.__quantity = quantity
        self.__price = price
        self.__symbol = symbol
    def get_quantity(self):
        return self._quantity
    def get_price(self):
        return self._price
    
    def get_symbol(self):
        return self.__symbol
    def set_quantity(self,quantity):
        self.__quantity = quantity
    def set_price(self,price):
        self.__price = price
    def set_symbol(self,symbol):
        self.__symbol = symbol
    def get_trade_value(self,price, quantity):
        return self.__price*self.__quantity

class TradeAccount:
   def __init__(self, name, starting_balance, trades, datetime):
       self.__name = name
       self.__starting_balance = starting_balance
       self.__current_balance = starting_balance
       self.__trades = []
       self.__datetime = dt.datetime.now()
   def get_current_balance(self):
        print('Your current balance is: ', self.__current_balance)
        return self.__current_balance
   def get_trades(self):
       for t in self.__trades:
           print(self.__trades[t])
       return len(self.__trades)
 
   def trade(self, side, price, quantity):
       if side:
           self.__current_balance -= (price*quantity)
           self.__trades.append(side)
       else:
           self.__current_balance += (price*quantity)
           self.__trades.append(side)
       return self.__current_balance

#Instantiate the class with a starting balance of 100 and no trades
ta1 = TradeAccount('JJ',100,[],dt.datetime.now()) 
st1 = Stock('MSFT',27,1,dt.datetime.now())   
st2 = Stock('CSCO',27,1,dt.datetime.now()) 
st3 = Stock('GOOG',27,1,dt.datetime.now()) 
st4 = Stock('SNAP',27,1,dt.datetime.now()) 


   

#Class to track the price history of a single stock
class Stock:
    def __init__(self, symbol, price, quantity, datetime):
        self.__symbol = symbol
        self.__price = price
        self.__quantity = quantity
        self.__datetime = datetime
        self.__price_history = {}
    def get_VWAP(self, symbol, stocks):
        pass

        
def get_price(symbol):
    #url = 'http://finance.yahoo.com/quote/'+symbol
    #response = requests.get(url)
    #parser = html.fromstring(response.text)
    #summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
    #summary_data = OrderedDict()
    other_details_json_link = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=financialData'.format(symbol)
    summary_json_response = requests.get(other_details_json_link)
    json_loaded_summary = json.loads(summary_json_response.text)
    return json_loaded_summary['quoteSummary']['result'][0]['financialData']['currentPrice']['raw']



       
def display_menu():
   
    for k,v in action_menu.items():
        print(k,':',v)
        

menu_option = 0    
#display_menu()

while menu_option >=0 and menu_option < 4:
        if menu_option == 0:
            display_menu()
        
        menu_option = int(input('Please select an option: '))
       
        if menu_option ==1:
            print('You chose', action_menu[menu_option])
            symbol = input('Type a ticker symbol')
            price = get_price(symbol)
            print('The price of', symbol, 'is',price)
            quantity = int(input('Enter quantity to buy: '))
            ta1.trade(BUY, price, quantity)
        elif menu_option==2:
            print('You chose', action_menu[menu_option])
            symbol = input('Type a ticker symbol') 
            price = get_price(symbol)
            print('The price of', symbol, 'is',price)
            quantity = int(input('Enter quantity to sell: '))
            ta1.trade(SELL, price, quantity)
        elif menu_option ==3: 
            print('You chose', action_menu[menu_option])
            ta1.get_current_balance()
            ta1.get_trades()
        elif menu_option ==4:
            print('You chose', action_menu[menu_option])
        #if the user typed something else reset menu option to 0
        #and give them another chance
        else:
            print('Invalid selection.  Please try again.')
            menu_option = 0
       
        
           
            



