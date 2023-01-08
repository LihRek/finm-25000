import os
import pandas as pd
import numpy as np

def histogram_weekly_losses(results):
    pnl_diff = results['Pnl'].diff(5)
    weekly_losses = pnl_diff[pnl_diff < 0]
    hist, _ = np.histogram(weekly_losses, bins = 50)
    return hist

def histogram_monthly_losses(results):
    pnl_diff = results['Pnl'].diff(20)
    monthly_losses = pnl_diff[pnl_diff < 0]
    hist, _ = np.histogram(monthly_losses, bins = 50)
    return hist 

def max_draw_down(results):
    drawdown_max_pnl = round(np.max(results['Pnl']), 2)
    return round(drawdown_max_pnl,2)

def histogram_position_holding_times(results):
    #calculate histogram for the position holding times

    # you can calculate the holding time this way:
    nrows = len(results)
    position_holding_times = []
    cur_holding_times = 0
    for i in range(0,nrows):
        if results.Position[i] != 0:
            cur_holding_times += 1
        elif cur_holding_times != 0:
            position_holding_times.append(cur_holding_times)
            cur_holding_times = 0
    hist, bins = np.histogram(position_holding_times, bins = 50)
    df = pd.DataFrame({'bins': bins[:-1], 'count': hist})
    df['bins'].round(2)
    df = df.set_index('bins')
    return df

def volatility_summary(results):
    # calculate weekly_pnls and the weekly_losses
    '''
    a = results.groupby(np.arange(len(results))//2).mean()
    weekly_pnls = list(a['Pnl'])
    '''
    pnl_diff = results['Pnl'].diff(5)
    weekly_losses = pnl_diff[pnl_diff < 0]
    sharpe_ratio = np.mean(weekly_pnls)/np.std(weekly_pnls,ddof=1)
    sortino_ratio = np.mean(weekly_pnls)/np.std(weekly_losses,ddof=1)
    # give the volatlity summary for:
    print('PnL Standard Deviation:', "{:.6f}".format(np.std(weekly_pnls, ddof=1)))
    print('Sharpe ratio:', "{:.6f}".format(sharpe_ratio))
    print('Sortino ratio:', "{:.6f}".format(sortino_ratio))
    pdf=pd.DataFrame([np.std(weekly_pnls,ddof=1),sharpe_ratio,sortino_ratio],
                     index=['PnL Standard Deviation','Sharpe ratio:','Sortino ratio:'],columns=['Summary'])
    return pdf


def traded_volume_summary(results):
    # calculate the total traded volume
    # traded_volume = np.abs( ) # you need to use the abs function on the correct field
    print('Total traded volume:', traded_volume)
    return traded_volume
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    test_function_name = input()
    rows_num = int(input().strip())
    data = []
    colnames = list(map(str, input().rstrip().split(',')))
    for i in range(rows_num):
        line = list(map(str, input().split(',')))
        line[0] = line[0]
        line[1] = float(line[1])
        line[2] = float(line[2])
        line[3] = float(line[3])
        line[4] = float(line[4])
        line[5] = float(line[5])
        line[6] = float(line[6])
        line[7] = float(line[7])
        line[8] = float(line[8])
        line[9] = float(line[9])
        line[10] = float(line[10])
        line[11] = float(line[11])
        line[12] = float(line[12])
        line[13] = float(line[13])
        
        data.append(line)    

    results = pd.DataFrame(data, columns = colnames)
    results.index=results['Date']

    
    res=globals()[test_function_name](results)
    fptr.write(str(res))
