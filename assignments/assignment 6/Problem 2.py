#!/bin/python3

import math
import os
import random
import re
import sys
import pandas as pd
import numpy as np
import statistics

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def case1(financial_data):
    print(financial_data.head(5))
    print(financial_data.tail(5))
    print(financial_data.describe())

def case2(financial_data):
    print(financial_data.resample('M').mean().head(5))

def case3(financial_data):
    print(financial_data[['Adj Close']].pct_change(1).dropna())

def case4(financial_data):
    print((1 + financial_data[['Adj Close']].pct_change(1).dropna()).cumprod())
    
def case5(financial_data):
    print((1 + financial_data[['Adj Close']].pct_change(1).dropna()).cumprod().resample('M').mean())

def case6(financial_data):
    print(financial_data[['Adj Close']].rolling(20).mean())

def case7(financial_data):
    print(financial_data[['Adj Close']].pct_change(1).rolling(100).std() * 10)

def case8(financial_data):
    signals = pd.DataFrame(columns = ['signal', 'short_mavg', 'long_mavg', 'orders'], index = financial_data.index)
    signals.loc[:, 'signal'] = 0.0
    signals.loc[:, 'short_mavg'] = financial_data['Close'].rolling(50, min_periods = 1).mean()
    signals.loc[:, 'long_mavg'] = financial_data['Close'].rolling(100, min_periods = 1).mean()
    signals['signal'].where(signals['short_mavg'] <= signals['long_mavg'], 1.0, inplace = True)
    signals['orders'] = signals['signal'].diff()
    if case_number == '8':
        print(signals)
    else:
        return signals
    
def case9(financial_data):
    signals = case8(financial_data)
    positions = pd.DataFrame(index = signals.index)
    positions['MSFT'] = 10 * signals['signal']
    portfolio = positions.multiply(financial_data['Adj Close'], axis = 0)
    portfolio['holdings'] = portfolio['MSFT']
    portfolio['cash'] = 10000 - (positions.diff().multiply(financial_data['Adj Close'], axis = 0)).sum(axis = 1).cumsum()
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()
    print(portfolio)

if __name__ == '__main__':
    case_number=input().strip()
    df = pd.read_csv(sys.stdin, header=0, index_col='Date', parse_dates=True)
    globals()['case'+case_number](df)
