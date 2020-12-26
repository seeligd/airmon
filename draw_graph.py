from pandas import read_csv
import seaborn as sns
import matplotlib.pylab as plt
plt.xticks(rotation=45)

series = read_csv('all.csv', header=0, parse_dates=[0], index_col=0, squeeze=True)
sns_plot = sns.lineplot(data=series)
fig = sns_plot.get_figure()
fig.set_size_inches(11.7, 8.27)
fig.savefig("output.png")
