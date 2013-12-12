__author__ = 'rebecca'

from bokeh.plotting import *

import datetime
import pandas
import pandas.io.data as web
import numpy as np


# Declare functions.

def sma(prices, n_periods):
    """
    Returns the rolling mean of a given list of stock prices "prices"
    over a period of time "n_periods". Interfaces with Pandas, so the details are
    sort of unknown to me.
    Return type: Array.
    """
    sma = pandas.rolling_mean(prices, n_periods, min_periods=n_periods)
    return sma  # Returns a Numpy array in this case


def bollinger_upper(prices, sma, n_periods):
    """
    Returns the upper Bollinger band line, for implementing a Bollinger
    band into the plot. Uses the list of stock prices "prices",
    the rolling mean returned by sma() "sma", over a number of periods "n_periods".
    You must use the same number of periods as used in the associated sma() function.
    Return type: Array.
    """
    stdev = pandas.rolling_std(prices, n_periods, min_periods=n_periods)
    return sma + (2 * stdev)  # Returns a Numpy Array in this case


def bollinger_lower(prices, sma, n_periods):
    """
    Returns the lower Bollinger band line, for implementing a Bollinger
    band into the plot. Uses the list of stock prices "prices",
    the rolling mean returned by sma() "sma", over a number of periods "n_periods".
    You must use the same number of periods as used in the associated sma() function.
    Return type: Array.
    """
    stdev = pandas.rolling_std(prices, n_periods, min_periods=n_periods)
    return sma - (2 * stdev)  # Returns a Numpy Array in this case


def rsi(prices, timeframe=14):
    """
    Returns the Relative Strength Index for a list of stock prices "prices"
    over a period of time "timeframe".
    Return type: Array.
    """

    delta = np.diff(prices)
    seed = delta[:timeframe+1]

    up = seed[seed >= 0].sum() / timeframe
    down = -seed[seed < 0].sum() / timeframe

    rs = up / down

    rsi = np.zeros_like(prices)
    rsi[:timeframe] = 100. - (100./(1.+rs))

    for i in range(timeframe, len(prices)):

        i_delta = delta[i-1]

        if i_delta > 0:
            upval = i_delta
            downval = 0.
        else:
            upval = 0.
            downval = -i_delta

        up = (up * (timeframe - 1) + upval) / timeframe
        down = (down * (timeframe - 1) + downval) / timeframe

        rs = up/down
        rsi[i] = 100. - (100. / (1. + rs))

    return rsi  # Returns a Numpy Array.


# Declare output file.

output_file('templates/stocks.html', title='How are my stocks doing today?', js='relative', css='relative')

# Define timespan.

start = datetime.date(2012, 1, 1)

end = datetime.date.today()

# Define periods (for SMA, Bollinger, etc.)

periods = 50

# List of symbols to look up.

symbols = ['AAPL', 'GOOG', 'MSFT', 'NTDOY']

# For each symbol in symbols:

for s in symbols:

    # Obtain the data.

    data = web.DataReader(s, 'google', start, end)

    close = data['Close'].values

    dates = data.index.values


    # Plot raw stock data.

    x = data.index

    y = close

    line(x, y, color='blue', x_axis_type='datetime')
    hold()

    # Perform TA on stock data.


    # Define SMA 50.

    sma50 = sma(close, periods)

    # Define Bollinger Bands.

    upperband = bollinger_upper(close, sma50, periods)

    lowerband = bollinger_lower(close, sma50, periods)

    # Define RSI.
    # TODO: Make this show up on the plot.

    rsi14 = rsi(close, 14)

    # Define RSI monitor.

    if rsi14[-1] <= 30:
        rsi_monitor = "BUY (OVERSOLD)"
    elif rsi14[-1] >= 70:
        rsi_monitor = "SELL (OVERBOUGHT)"
    else:
        rsi_monitor = "WAIT (STABLE)"

    # TODO: Add MACD.



    # Plot analyses.


    # SMA 50:

    line(x, sma50, color='red', x_axis_type='datetime')

    # Bollinger Band Lines:

    line(x, upperband, color='black', x_axis_type='datetime')

    line(x, lowerband, color='black', x_axis_type='datetime')

    # Bollinger shading glyph:

    reverse_upper = upperband[::-1]

    bandprice = np.append(lowerband, reverse_upper)

    banddates = np.append(dates, dates[::-1])

    patch(pandas.to_datetime(banddates), bandprice, color='#A6CEE3', fill_alpha=0.3, x_axis_type='datetime')

    # Remove hold, allow for more plots to be added.

    curplot().title = s

    grid().grid_line_alpha = 0.4

    hold()

# Finally, display all plots.

show()