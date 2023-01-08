import sys
import pandas as pd
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
import numpy as np
from statsmodels.tsa.stattools import coint

def zscore(series):
    return (series - series.mean()) / np.std(series)

# Enter your code here. Read input from STDIN. Print output to STDOUT
def calc_cointegration(data):
    # We will use Adj Close price
    data = data['Adj Close']
    n = data.shape[1] # dimension of the matrix
    #initiate your matrix here with value 1
    pvalue_matrix = np.ones((n, n))
    # get stock symbols from data using dataframe.columns
    symbols = data.columns
    # loop through symbols to get pairwise pvalue for cointegration test (you only need to calculate n*(n-1)/2 pvalues)
    # Please avoid hardcoding!
    for i in range(n):
        for j in range(i + 1, n):
            _, pvalue_matrix[i, j], _ = coint(data[symbols[i]], data[symbols[j]])
    return pvalue_matrix

def get_sample_data(data):
    df = pd.DataFrame(data = data)
    df = df.loc['2002-04-01':'2005-04-01', (['Adj Close'], ['MSFT', 'JNPR'])]
    df.columns = df.columns.droplevel()
    return df

def get_signal(data):
    data = get_sample_data(data)
    # You will build a new dataframe to display prices for two stocks, z_score and signals
    # check expected output for detail
    df = pd.DataFrame(columns = ['symbol1_price', 'symbol2_price', 'z_score', 'signal'])
    df['symbol1_price'] = data['MSFT']
    df['symbol2_price'] = data['JNPR']
    df['z_score'] = zscore(data['MSFT']/data['JNPR'])
    df['signal'] = 0
    df['signal'].where(df['z_score'] > -1, other = 1, inplace = True)
    df['signal'].where(df['z_score'] < 1, other = -1, inplace = True)
    return df
    
def pnl(data):
    df = get_signal(data)
    # calculate performance
    df['signal_diff'] = df['signal'].diff()
    df['holding'] = df['signal'] * (df['symbol1_price'] - df['symbol2_price'])
    df['cash'] = (0 - (df['signal_diff'].multiply((df['symbol1_price'] - df['symbol2_price']), axis = 0).cumsum())).fillna(0)
    df['total'] = df['holding'] + df['cash']
    return df

    

def test_calc_cointegration(data):
    print(calc_cointegration(data))
def test_get_sample_data(data):
    print(get_sample_data(data))
def test_get_signal(data):
    print(get_signal(data))
def test_pnl(data):
    df = pnl(data)
    df['holding'] = np.where(df['holding']!=0,df['holding'],0)
    print(df)

if __name__ == '__main__':
    func_name = input().strip()
    data = pd.read_csv(sys.stdin, header=[0,1],index_col=0, parse_dates=True)
    globals()[func_name](data)
