import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from IPython.display import display
dp = '{:.4f}'
pd.options.display.float_format = dp.format
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)

def maximumDrawdown(returns):
    cum_returns = (1 + returns).cumprod()
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns - rolling_max) / rolling_max

    max_drawdown = drawdown.min()
    end_date = drawdown.idxmin()
    summary = pd.DataFrame({'Max Drawdown': max_drawdown, 'Bottom': end_date})

    for col in drawdown:
        summary.loc[col, 'Peak'] = (rolling_max.loc[:end_date[col], col]).idxmax()
        recovery = (drawdown.loc[end_date[col]:, col])
        try:
            summary.loc[col, 'Recover'] = pd.to_datetime(recovery[recovery >= 0].index[0])
        except:
            summary.loc[col, 'Recover'] = pd.to_datetime(None)

        summary['Peak'] = pd.to_datetime(summary['Peak'])
        try:
            summary['Duration (to Recover)'] = (summary['Recover'] - summary['Peak'])
        except:
            summary['Duration (to Recover)'] = None

        summary = summary[['Max Drawdown', 'Peak', 'Bottom', 'Recover', 'Duration (to Recover)']]

    return summary

def performanceMetrics(returns,annualization = 12, quantile = .05):
    metrics = pd.DataFrame(index=returns.columns)
    metrics['Mean'] = returns.mean() * annualization
    metrics['Vol'] = returns.std() * np.sqrt(annualization)
    metrics['Sharpe'] = (returns.mean() / returns.std()) * np.sqrt(annualization)

    metrics['Min'] = returns.min()
    metrics['Max'] = returns.max()
    return metrics

def tailMetrics(returns, quantile=.05, relative=False, mdd=True):
    metrics = pd.DataFrame(index=returns.columns)
    metrics['Skewness'] = returns.skew()
    metrics['Kurtosis'] = returns.kurtosis() - 3

    VaR = returns.quantile(quantile)
    CVaR = (returns[returns < returns.quantile(quantile)]).mean()

    if relative:
        VaR = (VaR - returns.mean())/returns.std()
        CVaR = (CVaR - returns.mean())/returns.std()

    metrics[f'VaR ({quantile})'] = VaR
    metrics[f'CVaR ({quantile})'] = CVaR

    if mdd:
        mdd_stats = maximumDrawdown(returns)
        metrics = metrics.join(mdd_stats)

        if relative:
            metrics['Max Drawdown'] = (metrics['Max Drawdown'] - returns.mean())/returns.std()

    return metrics

# everything so far is helper functions from github

desc = pd.read_excel('data.xlsx', 'descriptions').rename(columns = {'Unnamed: 0':'Symbol'}).set_index('Symbol')
funds = pd.read_excel('data.xlsx','hedge_fund_series').set_index('date')
mlf = pd.read_excel('data.xlsx','merrill_factors').set_index('date')
other = pd.read_excel('data.xlsx','other_data').set_index('date')

# Problem 1 & 2
print(performanceMetrics(funds), '\n')
print(tailMetrics(funds))

# Problem 3
for regressand in funds.columns:
    x = sm.add_constant(pd.DataFrame(mlf['SPY US Equity']))
    y = pd.DataFrame(funds[regressand])
    model = sm.regression.linear_model.OLS(y, x).fit()
    print(model.summary(), '\n')
    var_res = model.resid.std()
    alpha = model.params[0]
    beta = model.params[1]
    ir = dp.format(alpha * np.sqrt(12) / var_res)
    tr = dp.format(funds[regressand].mean() * 12 / beta)
    print('beta =', dp.format(beta))
    print('information ratio =', ir)
    print('treynor ratio = ', tr)

# Problem 5
corr_matrix = funds.corr()
print("**** correlation matrix ****")
display(corr_matrix)
plt.figure(figsize = (12,8))
sns.heatmap(corr_matrix)
plt.show()

# Problem 6
x = sm.add_constant(pd.DataFrame(mlf))
y = pd.DataFrame(funds['HFRIFWI Index'])
model = sm.regression.linear_model.OLS(y, x).fit()
print(model.summary(), '\n')
scale = 1 / sum(model.params[1:7])
print('**** portfolio weights ****')
for i in range(1, 6):
    print(mlf.columns[i - 1], "{:.2f}".format(model.params[i] * scale))
print('r-squared =', dp.format(model.rsquared))

exp = scale * np.dot(mlf, model.params[1:7])
epsilon = (exp - funds['HFRIFWI Index']).std() * np.sqrt(12)
print('tracking error =', dp.format(epsilon))