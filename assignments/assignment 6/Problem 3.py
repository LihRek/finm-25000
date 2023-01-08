#!/bin/python3

import math
import os
import random
import re
import sys

from collections import deque



# Python program to get average of a list
def average(lst):
    return sum(lst) / len(lst)

class TradingStrategy:
    def __init__(self):
        self.small_window=deque()
        self.large_window=deque()
        self.long_signal=False
        self.position=0
        self.cash=10000
        self.total=0
        self.holdings=0

    def onPriceUpdate(self,price_update):
        date = price_update['date']
        close = price_update['close']
        adj = price_update['adjprice']
        
        self.small_window.append(close)
        self.large_window.append(close)
        if len(self.small_window) > 50:
            self.small_window.popleft()
        if len(self.large_window) > 100:
            self.large_window.popleft()

        if average(self.small_window) > average(self.large_window):
            self.long_signal = True
        else:
            self.long_signal = False
        
        if len(self.small_window) == 50:
            self.checkSignal(price_update)
                
    def checkSignal(self,price_update):
        date = price_update['date']
        close = price_update['close']
        adj = price_update['adjprice']
        
        if self.position == 0 and self.long_signal:
            print(f"{date} send buy order for 10 shares price={adj}")
            self.position += 10
            self.cash -= adj * 10
        
        if self.position > 0 and not self.long_signal:
            print(f"{date} send sell order for 10 shares price={adj}")
            self.position -= 10
            self.cash += adj * 10
        
        self.holdings = self.position * adj
        self.total = self.cash + self.holdings
        
        print('%s total=%d, holding=%d, cash=%d' %
              (price_update['date'],self.total, self.holdings, self.cash))
        

if __name__ == '__main__':
    
    ts=TradingStrategy()
    nb_of_rows = int(input().strip())
    market_data_header = input().strip()

    for _ in range(nb_of_rows):
        row = input().strip().split(',')
        ts.onPriceUpdate({'date' : row[0],
                              'close' : float(row[4]),
                              'adjprice' : float(row[6])})
