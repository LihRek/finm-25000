import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from sklearn.linear_model import LinearRegression
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)
pd.set_option('display.precision', 3)
sys.path.insert(0, '../cmds')

def ols(regressors, targets, annualization = 12, ignorenan = True):
    # ensure regressors and targets are pandas dataframes, as expected
    if not isinstance(regressors, pd.DataFrame):
        regressors = regressors.to_frame()
    if not isinstance(targets, pd.DataFrame):
        targets = targets.to_frame()

    # align the targets and regressors on the same dates
    df_aligned = targets.join(regressors, how='inner', lsuffix='y ')
    Y = df_aligned[targets.columns]
    Xset = df_aligned[regressors.columns]

    reg = pd.DataFrame(index=targets.columns)
    for col in Y.columns:
        y = Y[col]

        if ignorenan:
            # ensure we use only non-NaN dates
            alldata = Xset.join(y, lsuffix='X')
            mask = alldata.notnull().all(axis=1)
            y = y[mask]
            X = Xset[mask]
        else:
            X = Xset

        model = LinearRegression().fit(X, y)
        reg.loc[col, 'alpha'] = model.intercept_ * annualization
        reg.loc[col, 'beta-' + regressors.columns] = model.coef_
        reg.loc[col, 'r-squared'] = model.score(X, y)

        # sklearn does not return the residuals, so we need to build them
        yfit = model.predict(X)
        residuals = y - yfit
        # Treynor Ratio is only defined for univariate regression
        if Xset.shape[1] == 1:
            reg.loc[col, 'Treynor Ratio'] = (y.mean() / model.coef_) * annualization

        # if intercept =0, numerical roundoff will nonetheless show nonzero Info Ratio
        num_roundoff = 1e-12
        if np.abs(model.intercept_) < num_roundoff:
            reg.loc[col, 'Info Ratio'] = None
        else:
            reg.loc[col, 'Info Ratio'] = (model.intercept_ / residuals.std()) * np.sqrt(annualization)
    return reg

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

def perf(returns, annualization = 12, quantile = .05):
    metrics = pd.DataFrame(index=returns.columns)
    metrics['Mean'] = returns.mean() * annualization
    metrics['Vol'] = returns.std() * np.sqrt(annualization)
    metrics['Sharpe'] = (returns.mean() / returns.std()) * np.sqrt(annualization)

    metrics['Min'] = returns.min()
    metrics['Max'] = returns.max()
    return metrics

def tail(returns, quantile=.05, relative=False, mdd=True):
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

returns0 = pd.read_excel('/Users/lihrek/Desktop/FINM 25000/Assignment 4/gmo_analysis_data.xlsx', sheet_name = 'returns (total)').set_index('Date')
rfr = pd.read_excel('/Users/lihrek/Desktop/FINM 25000/Assignment 4/gmo_analysis_data.xlsx', sheet_name = 'risk-free rate').set_index('Date') / 12
#returns0 = returns0.subtract(rfr['US3M'], axis = 0)
returns1 = returns0.loc[:'2011']
returns2 = returns0.loc['2012':]

print("**** problem 2.1 ****")
df0 = perf(returns0)
df1 = perf(returns1)
df2 = perf(returns2)
performance = pd.concat([df1, df2, df0], keys = ["1996-2011", "2012-2022", "1996-2022"])
print(performance)
print("since the case, GMWAX's mean has increased while vol has decreased, leading to an increase in sharpe ratio", "\n")

print("**** problem 2.2 ****")
df0 = tail(returns0)
df1 = tail(returns1)
df2 = tail(returns2)
drawdown = pd.concat([df1, df2, df0], keys = ["1996-2011", "2012-2022", "1996-2022"])
drawdown.style.format({
    'Skewness': '{:.2f}',
    'Kurtosis': '{:.2f}',
    'VaR (0.05)': '{:.2f}',
    'CVaR (0.05)': '{:.2f}',
    'Max Drawdown': '{:.2f}',
    'Peak': '{:%Y-%m}',
    'Bottom': '{:%Y-%m}',
})
print(drawdown)
print("as seen in the lower (closer to 0) VaR, CVaR and max drawdown, GMWAX has somewhat lower tail risk")
print("this did not vary much across the two subsamples")
print("however, it is noteworthy that it took GMWAX longer to recover in each of the cases")
print("furthermore, while the max drawdown for GMWAX occured in 2001, it occured for SPY in 2009, during the financial crisis", '\n')

print("**** problem 2.3 ****")
df0 = ols(returns0[['SPY']], returns0[['GMWAX']])
df1 = ols(returns1[['SPY']], returns1[['GMWAX']])
df2 = ols(returns2[['SPY']], returns2[['GMWAX']])

reg = pd.concat([df1, df2, df0], keys = ["1996-2011", "2012-2022", "1996-2022"])
print(reg)
print('market beta around 0.5 is significant; beta has not changed significantly after the case')
print('GMWAX provided a positive alpha close to 0, which has worsened significantly after the case and dipped into the negatives')
print('this means that GMWAX consistently underperforms compared to SPY, and has gotten worse since the case', '\n')

print("**** problem 3.1 ****")
signals = pd.read_excel('/Users/lihrek/Desktop/FINM 25000/Assignment 4/gmo_analysis_data.xlsx', sheet_name = 'signals').set_index('Date')
signalsl = signals.shift().dropna()
signalsl, spy = signalsl.align(returns0[['SPY']], join = 'inner', axis = 0)
forecasts = returns0[['SPY']].expanding().mean().shift(1).dropna()
forecasts.columns = ['Mean']
model_map = {'DP': ['DP'], 'EP': ['EP'], 'ALL': signals.columns}
for model in model_map.keys():
    X = signalsl[model_map[model]]
    forecasts[model] = LinearRegression().fit(X, spy).predict(X)
    print(ols(X, spy))
forecasts.dropna(inplace = True)
fig, ax = plt.subplots(figsize = (12,6))
forecasts.plot(ax = ax)
plt.legend(forecasts.columns)
plt.title('Forecasted Return')
plt.ylim(-.005,.03)
print('\n')

print("**** problem 3.2 ****")
fund_returns = forecasts * 100 * spy.values
fund_returns.insert(0, 'Passive', spy)
print('correlation of funds performances:')
fund_returns.corr().style.format('{:,.1%}'.format)
print(fund_returns.corr(), '\n')

(fund_returns + 1).cumprod().plot(figsize = (10,5), title = 'cumulative Returns of Strategies')
corr_rolling = fund_returns.rolling(60).corr()
dynamic_corrs = (corr_rolling['Passive'].unstack(1))
dynamic_corrs = dynamic_corrs.reindex(columns=fund_returns.columns).drop(columns=['Passive'])
dynamic_corrs.plot(figsize=(10, 5), title='correlation to SPY');

print("performance and tail metrics:")
performance = perf(fund_returns)
print(performance)
performance = tail(fund_returns)
print(performance, '\n')

print("regression:")
performance = ols(spy, fund_returns, annualization = 12)
print(performance, '\n')

print("**** problem 3.3 - 3.5 ****")
comp = (fund_returns['2000':'2011'] + 1).cumprod()
comp['RF'] = (rfr['2000':'2011'] * 12 + 1).cumprod()
comp.plot(figsize=(10, 5), title = 'Stocks vs RFR')
plt.show()
print("as shown in the plot, only ALL outperfoms the RFR while DP and EP slightly underperform it")





