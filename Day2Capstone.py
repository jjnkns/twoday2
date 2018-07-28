# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 12:44:34 2018

@author: jjnkn 
Jennifer Jenkins
For Chainhaus two day Python Blockchain Data Science Intro class
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

import requests
import json
import datetime as dt
import hashlib

import pandas as pd
import pickle

with open('data.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    data = pickle.load(f)
    print('Here is proof that we have pickled data from before:',data)

action_menu = {1:'Buy',2:'Sell',3:'View Balance',4:'Exit'}
current_transact_count = 0
max_transact_count = 5
transaction_list=[]

#initialize booleans for trade sides
BUY = True
SELL = False

class TradeAccount:
   def __init__(self, name, initial_balance, datetime):
       self.__name = name
       self.__initial_balance = initial_balance
       self.__current_balance = initial_balance
       self.__datetime = dt.datetime.now()
       self.__balance_history = []
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

   def get_trade_count(self):
       return len(self.__balance_history)
    
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
      
  def get_transactions(self):
      return self.__transactions
      print(self.__transactions.count)
      

#Start a new block from scratch
genesis = Block(0,0,transaction_list)
print(genesis.__dict__)


#Instantiate the class with a starting balance of 500000 and no trades
ta1 = TradeAccount('JJ',500000, dt.datetime.now()) 

#Class to track the price history of a single stock
#for this exercise let's pretend that we are getting real time price instead of closing price
class Stock:
    def __init__(self, price_history):
        self.__price_history = []
    def add_price_history(self,price_history):
        self.__price_history.append(price_history)
    def get_vwap(self,symbol):
        #print('HISTORY:',self.__price_history)
        running_q = 0 #initialize running value for quantity
        running_qp =0 #initialize running value for quantity * price
        
        for h in range(0,len(self.__price_history)):
           json_data=self.__price_history[h]
           df=pd.read_json(json_data, typ='series')
           if df['symbol']==symbol:
               q = int(df['quantity'])
               p = float(df['price'])
               qp = q*p
           
               running_q +=q
               running_qp +=qp
               vwap = running_qp/running_q
               return vwap
       


price_history ={}
#instantiate to track stock prices
stock1 = Stock(price_history)

        
def get_price(symbol):
  
    other_details_json_link = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=financialData'.format(symbol)
    summary_json_response = requests.get(other_details_json_link)
    json_loaded_summary = json.loads(summary_json_response.text)
    return json_loaded_summary['quoteSummary']['result'][0]['financialData']['currentPrice']['raw']
       
def display_menu():
   
    for k,v in action_menu.items():
        print(k,':',v)
        
menu_option = 0    

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
           
          #note that when running this after hours we get the same price and vwap over and over
          #in real life intraday vwap will be dynamic
          #to test this we could use a random numbers or stock price history instead
            if menu_option == 1:
                quantity = int(input('Enter quantity to buy: '))
                side = 'BUY'
                print('Trade value: $',price*quantity)  
                balance = ta1.trade(BUY, price, quantity)
                
            else:
                quantity = int(input('Enter quantity to sell: '))
                side = 'SELL'
                print('Trade value: $',price*quantity) 
                balance = ta1.trade(SELL, price, quantity)
                
            #build a string concatenating the parameters
            json_data = '{"time":"'+str(dt.datetime.now()) +'",'+'"symbol":"'+symbol+'","price":'+str(price)+ ',"quantity":'+str(quantity)+',"side":"'+side+'"}'
            transactions = json.loads(json_data) 
            stock1.add_price_history(json_data) #add to stocks so we can get vwap
            print('VWAP for', symbol, ' is now: $', stock1.get_vwap(symbol))
            
            #build the list of trades until you get to max. print running list to demonstrate it is working
            if len(transaction_list)<max_transact_count:
                transaction_list.append(transactions)
                for n in range(0,len(transaction_list)):
                    print(transaction_list[n])
            
            #once we have max number trades allowed per block
            #write them to a block, pickle the data, clear the list and start a new block
            if len(transaction_list)==max_transact_count:
                with open('data.pickle', 'wb') as f:
                    # Pickle the 'data' dictionary using the highest protocol available.
                    pickle.dump(transaction_list, f, pickle.HIGHEST_PROTOCOL)
                    trade_count = ta1.get_trade_count() #how many trades overall
                    if trade_count==max_transact_count*1: #first n trades go in first block
                        block1 = Block(1,genesis.get_hash(),transaction_list)
                        print(block1.__dict__)
                    elif trade_count==max_transact_count*2:#next n trades go into a new block
                        block2 = Block(2,block1.get_hash(),transaction_list)
                        print(block2.__dict__)
                    elif trade_count==max_transact_count*3:#next n trades go into a new block
                        block3 = Block(3,block2.get_hash(),transaction_list)
                        print(block3.__dict__)
                transaction_list.clear()
     
        elif menu_option ==3: 
            ta1.get_current_balance()
       
        elif menu_option ==4:
            print('Good bye')
        #if the user typed something else reset menu option to 0
        #and give them another chance
        else:
            print('Invalid selection.  Please try again.')
            menu_option = 0
       
        
           
            



