from pandas import read_csv
import seaborn as sns
import matplotlib.pylab as plt
plt.xticks(rotation=45)

series = read_csv('all.csv', header=0, parse_dates=[0], index_col=0, squeeze=True)

series['AQI (PM2.5) 1H'] = series['AQI (PM2.5)'].rolling(window='1H').mean()
series['AQI (PM2.5) 24H'] = series['AQI (PM2.5)'].rolling(window='24H').mean()

sns_plot = sns.lineplot(data=series)
sns_plot.axhline(y = 50, color='gray', linewidth=1, alpha=.2, label='good')
sns_plot.axhline(y = 100, color='gray', linewidth=1, alpha=.2, label='moderate')

fig = sns_plot.get_figure()
fig.set_size_inches(11.7, 8.27)
fig.savefig("output.png")
