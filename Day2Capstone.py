# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 12:44:34 2018

@author: jjnkn
"""


#Build a trading application that can scrape quotes from a website (i.e finance.yahoo.com)
#The user can buy, sell, view trades and view current  cash balance
#Store the trade information  on a custom blockchain (i.e. 10 trades per block)
#Store a real-time profit / loss for each stock using dictionaries and VWAP algorithm
#Read up on Python pickling and find a mechanism to store the blockchain to disk and retrieve it even after the app is stopped and restarts. Feel free to use JSON format.

#VWAP = volume-weighted average price
#price multiplied by number of shares traded and then dividing by the total shares traded for the day.
#Read up on Python pickling and find a mechanism to store the blockchain to disk
#and retrieve it even after the app is stopped and restarts. Feel free to use JSON format.'''

#from http://empirica.io/blog/vwap-algorithm/
#typical price = close + high + low divided by 3
#or open + close + high + low divided by 4

import requests
import json
import datetime as dt
import hashlib

import pandas as pd
import pickle



action_menu = {1:'Buy',2:'Sell',3:'View Balance',4:'Exit'}
current_transact_count = 0
max_transact_count = 10
transaction_list=[]

#initialize booleans for trade sides
BUY = True
SELL = False


class Trade:
    def __init__(self, quantity, price, symbol, timestamp):
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
    def add_trade_history(self, quantity, price, symbol, timestamp):
        col_names = ['symbol','price', 'quantity', 'PxQ', 'timestamp']
        data = [symbol, price, quantity, price*quantity,dt.datetime.now()]
        df = pd.DataFrame(data,columns=col_names)
        Total = df['PxQ'].sum()
        return Total
    

class TradeAccount:
   def __init__(self, name, initial_balance, datetime):
       self.__name = name
       self.__initial_balance = initial_balance
       self.__current_balance = initial_balance
       self.__datetime = dt.datetime.now()
       self.__balance_history = []
       self.__price_history = []
   def get_current_balance(self):
        print('Your current balance is: ', self.__current_balance)
        
        print('Trades made: ', len(self.__balance_history))
        print('Initial balance: $' + str(self.__initial_balance))
        print('Profit Loss: $' + str(self.__current_balance - self.__initial_balance))
        print('Ending balance: $' + str(self.__current_balance))
        
        if len(self.__balance_history)>0:
            print('Min balance: $' + str(min(self.__balance_history)))
            print('Max balance: $' + str(max(self.__balance_history)))
            print('Average balance: $' + str(sum(self.__balance_history) /
                                        len(self.__balance_history)))
        return self.__current_balance
     
   def trade(self, side, price, quantity):
       trade_value = price*quantity
       if side: #BUY
           balance = self.__current_balance - trade_value
       else: #SELL
           balance = self.__current_balance + trade_value
       self.__current_balance = balance
       self.__balance_history.append(balance)
     
       return self.__current_balance



class Block:
  def __init__ (self, seq_id, prev_hash, transactions):
    self.__seq_id = seq_id
    self.__created = dt.datetime.now()
    self.__prev_hash = prev_hash
    self.__transactions = transactions
    self.__hash = self.__gen_hash()

  def __gen_hash(self):
    sha = hashlib.sha256()
    metadata = str(self.__seq_id) + " " + str(self.__created) + " " + str(self.__prev_hash) + str(self.__transactions)
    metadata = metadata.encode('utf-8')
    sha.update(metadata)
    return sha.hexdigest()

  def get_hash(self):
    return self.__hash

  def add_transaction(self, side,price,quantity): #Add a dictionary
      col_names = ['Side','Price','Quantity']
      df = pd.DataFrame(columns=col_names)
      data = pd.DataFrame([[side, price, quantity]],columns=col_names)
      df = df.append(data, ignore_index=True)
      self.__transactions = df.items()
      
  def get_transactions(self):
      return self.__transactions
      print(self.__transactions.count)
      
        
class Blockchain:

 #def add_transaction(transactions):
 #   block = Block()
  
  def __get_seq_id():
    return 


chain = Blockchain()
#chain.add_transaction(transaction)
columns = ["high","low","open","close"]
transactions = ([0,0,0],['Side','Price','Quantity'])


genesis = Block(0,0,transactions)
print(genesis.__dict__)


block1 = Block(1,genesis.get_hash(),transactions)
print(block1.__dict__)




#Instantiate the class with a starting balance of 100 and no trades
ta1 = TradeAccount('JJ',500000, dt.datetime.now()) 



   

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
  
    other_details_json_link = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=financialData'.format(symbol)
    summary_json_response = requests.get(other_details_json_link)
    json_loaded_summary = json.loads(summary_json_response.text)
    return json_loaded_summary['quoteSummary']['result'][0]['financialData']['currentPrice']['raw']
       
def display_menu():
   
    for k,v in action_menu.items():
        print(k,':',v)
        
menu_option = 0    

t1 = Trade('x',0,0,dt.datetime.now())

while menu_option >=0 and menu_option < 4:
        if menu_option == 0:
            display_menu()
        #Here I would prefer to not repeat code that is the same for buy and sell
        menu_option = int(input('Please select an option: '))
        print('You chose', action_menu[menu_option])
        if menu_option ==1 or menu_option == 2:
            symbol = input('Type a ticker symbol')
            price = get_price(symbol)
            print('The price of', symbol, 'is',price)
            block1 = Block(1,genesis.get_hash(),transactions)
            #print(block1.__dict__)
                 
            if menu_option == 1:
                quantity = int(input('Enter quantity to buy: '))
                print('Trade value: $',price*quantity)  
                balance = ta1.trade(BUY, price, quantity)
                
            else:
                quantity = int(input('Enter quantity to sell: '))
                print('Trade value: $',price*quantity) 
                balance = ta1.trade(SELL, price, quantity)
            #build a string concatenating the parameters
            json_data = '{"symbol":"'+symbol+'","price":"'+str(price)+'","quantity":"'+str(quantity)+'"}'
            print(json_data)
            transactions = json.loads(json_data)
            print(transactions['symbol'],transactions['price'])
            transaction_list.append(transactions)
            for n in range(0,len(transaction_list)):
                print(transaction_list[n])
            #once we have 10 trades write them to a block
            if len(transaction_list)==10:
                block1 = Block(1,genesis.get_hash(),transaction_list)
                print(block1.__dict__)
                
     
        elif menu_option ==3: 
            ta1.get_current_balance()
       
        elif menu_option ==4:
            print('Good bye')
        #if the user typed something else reset menu option to 0
        #and give them another chance
        else:
            print('Invalid selection.  Please try again.')
            menu_option = 0
       
        
           
            



