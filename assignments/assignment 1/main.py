import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# import data
data = pd.read_excel("data.xlsx", sheet_name='excess returns').set_index('Date')
data.index = pd.to_datetime(data.index)

# question 1
perf = data.describe().loc[['mean', 'std']].transpose()
perf['mean'] *= 12
perf['std'] *= np.sqrt(12)
perf['sr'] = perf['mean']/perf['std']

display(perf)
max_sr = max(perf['sr'])
print("maximum sr:",perf.index[int(np.where(perf['sr'] == max_sr)[0])], "with sr =", max_sr)
min_sr = min(perf['sr'])
print("minimum sr:",perf.index[int(np.where(perf['sr'] == min_sr)[0])], "with sr =", min_sr)

# question 2
c_matrix = data.corr()
print("\n", '***** Correlation Matrix *****', "\n")
display(c_matrix)
plt.figure(figsize = (6,4))
sns.heatmap(c_matrix)
plt.show()
