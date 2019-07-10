from common.td import TD
from common.utils import Utils

import os
import logging
import datetime
import pandas as pd
import numpy as np
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

logger = logging.getLogger()
logger.setLevel(logging.INFO)

td_client = TD()
utils = Utils()

def main():
    # Get list of stocks to investigate
    movers = td_client.get_movers()

    valid = []
    watchlist = ['AMD', 'UGAZ', 'DGAZ', 'GUSH', 'DRIP', 'SQQQ', 'TQQQ', 'UWT', 'DWT', 'JNUG', 'JDST']

    for stock in movers:
        if stock['totalVolume'] > 100000 and stock['last'] > 10:
            valid.append(stock['symbol'])

    stocks = valid + watchlist

    logger.info("Stocks of interest: {}".format(stocks))

    # Clear charts folder
    utils.archive_charts()

    logger.info("Moved charts from charts/ to archives/")

    # Run analysis for stocks
    focus = []

    # Uniform start and end times
    end = datetime.datetime.now().timestamp() * 1000
    start = end - 2592000000

    logger.info("Getting historic data from {} to {}".format(start, end))

    for stock in stocks:
        # Get 30 months of data
        data = td_client.get_price_history(symbol=stock, period_type='day', period=10, frequency_type='minute',
                                           frequency=1, start_date=int(start), end_date=int(end),
                                           needExtendedHoursData=True)

        df = pd.DataFrame.from_dict(data)
        df = pd.concat([df.drop(['candles'], axis=1), df['candles'].apply(pd.Series)], axis=1)

        df['date'] = df['datetime'].apply(
            lambda x: datetime.datetime.fromtimestamp(x / 1000.0).strftime('%Y-%m-%d %H:%M'))
        df = df.set_index('date')

        # Define color scheme
        INCREASING_COLOR = 'g'
        DECREASING_COLOR = 'r'

        # Focusing on 1 day worth of data
        start_chart = datetime.datetime.fromtimestamp((end - 86400000) / 1000.0).strftime('%Y-%m-%d %H:%M')
        df_trim = df[df.index >= start_chart]

        # Creating core candlestick graph
        data = [dict(
            type='candlestick',
            open=df_trim['open'],
            high=df_trim['high'],
            low=df_trim['low'],
            close=df_trim['close'],
            x=df_trim.index,
            yaxis='y2',
            name='Historic Data',
            increasing=dict(line=dict(color=INCREASING_COLOR)),
            decreasing=dict(line=dict(color=DECREASING_COLOR)),
        )]

        layout = dict()

        fig = dict(data=data, layout=layout)

        # Setting graph details
        fig['layout'] = dict()
        fig['layout']['plot_bgcolor'] = 'rgb(250, 250, 250)'
        fig['layout']['xaxis'] = dict(rangeselector=dict(visible=True), autorange=True)
        fig['layout']['yaxis'] = dict(domain=[0, 0.2], showticklabels=False, autorange=True)
        fig['layout']['yaxis2'] = dict(domain=[0.2, 0.8])
        fig['layout']['legend'] = dict(orientation='h', y=0.9, x=0.3, yanchor='bottom')
        fig['layout']['margin'] = dict(t=40, b=40, r=40, l=40)

        # Defining range selector
        rangeselector = dict(
            visibe=True,
            x=0, y=0.9,
            bgcolor='rgba(150, 200, 250, 0.4)',
            font=dict(size=13),
            buttons=list([
                dict(count=1,
                     label='reset',
                     step='all'),
                dict(count=1,
                     label='1 yr',
                     step='year',
                     stepmode='backward'),
                dict(count=3,
                     label='1 month',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                     label='1 day',
                     step='day',
                     stepmode='backward'),
                dict(step='all')
            ]))

        fig['layout']['xaxis']['rangeselector'] = rangeselector

        # Add EMA lines
        df['9_day_ema'] = df['close'].ewm(span=9, adjust=False).mean()
        df['20_day_ema'] = df['close'].ewm(span=20, adjust=False).mean()

        df_trim = pd.merge(df_trim, df[['9_day_ema', '20_day_ema']], how='left', left_index=True, right_index=True)

        mv_y = df_trim['9_day_ema']
        mv_x = list(df_trim.index)

        fig['data'].append(dict(x=mv_x, y=mv_y, type='scatter', mode='lines',
                                line=dict(width=1),
                                marker=dict(color='#2ca02c'),
                                fill=None,
                                yaxis='y2', name='9 Day Exp Moving Average'))

        mv_y = df_trim['20_day_ema']
        mv_x = list(df_trim.index)

        fig['data'].append(dict(x=mv_x, y=mv_y, type='scatter', mode='lines',
                                line=dict(width=1),
                                marker=dict(color='#17becf'),
                                fill=None,
                                yaxis='y2', name='20 Day Exp Moving Average'))

        # Highlight where 9 day EMA is greater than 20 day EMA
        df_trim['cross'] = np.where(df_trim['9_day_ema'] - df_trim['20_day_ema'] >= df_trim['close'] * .0005,
                                    df_trim['close'] * 1.05, None)

        mv_y = df_trim['cross']
        mv_x = list(df_trim.index)

        fig['data'].append(dict(x=mv_x, y=mv_y, type='scatter', mode='lines',
                                line=dict(width=3),
                                marker=dict(color='#00FF00'),
                                yaxis='y2', name='Buy'))

        # Add volume bars
        fig['data'].append(dict(x=df_trim.index, y=df_trim['volume'],
                                marker=dict(color='#6B5B95'),
                                type='bar', yaxis='y', name='Volume'))

        end_date = datetime.datetime.fromtimestamp(end / 1000.0).strftime('%Y-%m-%d %H:%M')
        workspace = os.getcwd()
        chart = plot(fig, filename=os.path.join(workspace, 'charts/{}.html'.format(stock + '_' + end_date)), validate=False, auto_open=False)


main()