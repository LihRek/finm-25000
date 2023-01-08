#!/bin/python3
import math
import os
import random
import re
import sys
import datetime
import pandas as pd
import numpy as np
import random
random.seed(6666)

def random_data(financial_data):
    signals = pd.DataFrame(columns = ['signal', 'orders'])
    signals.loc[0] = [0, np.nan]
    for i in range(1, row_num):
        if i % 4 == 0:
            line = [0, -1.0]
        elif i % 4 == 1:
            line = [1, 1.0]
        else:
            line = [1, 0.0]
        signals.loc[i] = line
    signals = signals.astype({'signal': 'int'})
    return signals

def calculate_holding_cash(financial_data,signals):
    positions = pd.DataFrame(columns = ['stock', 'holdings', 'cash', 'total', 'returns'])
    positions.loc[0] = [0, 0, 10000, 10000, np.nan]
    q, s, c, t = 0, 0, 10000, 10000
    for i in range(1, row_num):
        price = financial_data.loc[i, 'Close']
        order = signals.loc[i, 'orders'] * 10
        q += order
        c -= order * price
        s = q * price
        
        t_new = s + c
        r = (t_new - t) / t
        t = t_new
        positions.loc[i] = [s, s, c, t, r]
    return positions


def test1(data):
    df=random_data(data)
    fptr.write(df.to_string())

def test2(data):
    df=random_data(data)
    portfolio=calculate_holding_cash(data,df)
    fptr.write(portfolio.to_string())
    

if __name__ == '__main__':
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')
    fptr = sys.stdout
    tmp = input()
    row_num = int(input().strip())
    Data = []
    col_names = list(map(str, input().split('\t')))
    for i in range(row_num):

        line=list(map(str, input().split('\t')))
        line[0] = pd.to_datetime(line[0])
        line[1] = float(line[1])
        line[2] = int(line[2])
        Data.append(line)
    data = pd.DataFrame(Data, columns= col_names)
    data.set_index('Date')
    
    if tmp == '1':
      test1(data)
    elif tmp == '2':
      test2(data)
    else:
      raise RuntimeError('invalid input')
