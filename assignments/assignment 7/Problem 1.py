import os
import pandas as pd
import datetime

def calculate_sentiment(df_sa):
    unique_ticker = df_sa['Ticker'].unique()
    values = []
    for ticker in unique_ticker: 
        dataframe = df_sa[df_sa['Ticker'] == ticker].set_index('Ticker').drop(columns = ['Headline'])
        mean = round(dataframe['compound'].mean(), 2)
        values.append(mean)
    
    df = pd.DataFrame(data = {'Ticker': unique_ticker, 'Mean Sentiment': values}).set_index('Ticker').sort_values(by = 'Mean Sentiment', ascending = False)
    return df
def test1(df_sa):
    c = calculate_sentiment(df_sa)
    fptr.write(c.to_string())

def test2(df_sa):
    c = calculate_sentiment(df_sa)
    fptr.write(c.to_string())

def test3(df_sa):
    c = calculate_sentiment(df_sa)
    fptr.write(c.to_string())

def test4(df_sa):
    c = calculate_sentiment(df_sa)
    fptr.write(c.to_string())


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    tmp = input()
    rows_num = int(input().strip())
    
    data = []
    colnames = list(map(str, input().rstrip().split('\t')))
    for i in range(rows_num):
        line = list(map(str, input().split('\t')))
        line[0] = line[0]
        line[1] = line[1]
        line[2] = line[2]
        line[3] = line[3]
        line[4] = line[4]
        line[5] = line[5]
        line[6] = float(line[6])
        line[7] = float(line[7])
        line[8] = float(line[8])
        line[9] = float(line[9])
        data.append(line)    

    df_sa = pd.DataFrame(data, columns = colnames)  
    
    if tmp == '1':
        test1(df_sa)
    elif tmp == '2':
        test2(df_sa)
    elif tmp == '3':
        test3(df_sa)
    elif tmp == '4':
        test4(df_sa)
    else:
        raise RuntimeError('invalid input')
