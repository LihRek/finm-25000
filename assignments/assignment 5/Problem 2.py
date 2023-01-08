import math
import os
import random
import re
import sys
import pandas as pd
import numpy as np
def case1(financial_data):
    financial_data = financial_data.sort_values('Date')
    # Print First 5 rows of MSFT
    print(financial_data.head(5))
    # Print Last 5 rows of MSFT
    print(financial_data.tail(5))

def case2(financial_data):
    #Resample to monthly data mean
    print(financial_data.resample('M').mean().head(5))
    #Display the first 5 rows

def case3(financial_data):
    # Create a variable daily_close and copy Adj Close from financial_data
    daily_close = financial_data[['Adj Close']]
    # Print first 20 daily returns
    print(daily_close.pct_change(1).head(20))
    
def case4(financial_data):
    # Calculate the cumulative daily returns
    # day1 : return1  cumulative reuturn : (1+return1)-1
    # day2 : return2  cumulative reuturn : (1+return1)*(1+return2)-1
    ret = financial_data[['Adj Close']].pct_change(1)
    print(((1+ret).cumprod()-1).head(20))
    # Print first 20 rows

def case5(financial_data):
    # Isolate the adjusted closing prices and store it in a variable
    # Calculate the moving average for a window of 20
    # Display the last 20 moving average number
    adj_close = financial_data[['Adj Close']]
    ma = adj_close.rolling(20).mean()
    print(ma.dropna().tail(20))

def case6(financial_data):
    # Calculate the volatility for a period of 100 don't forget to multiply by square root
    ret = financial_data[['Adj Close']].pct_change(1)
    ret1 = (((1+ret).cumprod()-1))
    vol = ret.rolling(100).std()*(10)
    # don't forget that you need to use pct_change
    # Print last 20 rows
    print(vol.dropna().tail(20))
if __name__ == '__main__':
    case_number=input().strip()
    df = pd.read_csv(sys.stdin, header=0, index_col='Date', parse_dates=True)
    globals()['case'+case_number](df)
    
