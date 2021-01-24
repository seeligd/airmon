from pandas import read_csv
import seaborn as sns
from datetime import datetime, timedelta


def draw_eink_graph(inputPath, outputPath):
    ago_24h = datetime.now() - timedelta(hours = 24)
    HEIGHT = 176
    WIDTH = 264

    df = read_csv(inputPath, header=0, parse_dates=[0], index_col=0, squeeze=True)
    df['AQI (PM2.5) 24H'] = df['AQI (PM2.5)'].rolling(window='24H').mean()
    df['AQI (PM2.5) 1H'] = df['AQI (PM2.5)'].rolling(window='.25H').mean()
    # PM10 seems lower in my region and makes the graph much busier, so keep it out
    # df['AQI (PM10) 24H'] = df['AQI (PM10)'].rolling(window='24H').mean()
    df['AQI (PM10) 1H'] = df['AQI (PM10)'].rolling(window='.25H').mean()

    df = df.loc[ago_24h:datetime.now()]

    # we only actually care about AQI
    f = df.drop(columns=['PM2.5', 'PM10', 'AQI (PM2.5)', 'AQI (PM10)'], axis=1)

    sns_plot = sns.lineplot(data=f)
    sns_plot.axhline(y = 50, linewidth=1, alpha=1, label='good', linestyle='--')
    sns_plot.axhline(y = 100, linewidth=1, alpha=1, label='moderate', linestyle='--')
    sns_plot.legend_.remove()
    sns_plot.set(xticklabels=[])
    sns_plot.set(xlabel=None)

    fig = sns_plot.get_figure()

    DPI = fig.get_dpi()
    fig.set_size_inches(WIDTH/float(DPI),HEIGHT/float(DPI))
    fig.savefig(outputPath)

if __name__ == "__main__":
    draw_eink_graph()
