__author__ = 'rebecca'

from bokeh.plotting import *

import pandas
import pandas.io.data as web
import shutil
import os
from pyta import *


# Create a plot for each symbol.

def build_plot(symbol, periods, start, end):

    file_name = '%s.html' % symbol

    output_file(file_name, title='How are my stocks doing today?')

    data = web.DataReader(symbol, 'google', start, end)

    close = data['Close'].values  # Returns Numpy array.

    dates = data.index.values  # Returns Numpy array.


    # Plot raw stock data.

    x = data.index

    y = close

    line(x[50:], y[50:], width=800, height=600, color='#1B9E77', x_axis_type='datetime')
    hold()


    # Perform TA on stock data.


    # Define SMA 50.

    sma50 = sma(close, periods)

    # Define Bollinger Bands.

    upperband = bollinger_upper(close, sma50, periods)

    lowerband = bollinger_lower(close, sma50, periods)

    # Define RSI.

    rsi50 = rsi(close)

    # Define MACD Line, Signal, and Histogram.

    macd = macd_line(close)

    signal = macd_signal(close)

    hist = macd_hist(close)


    # Plot analyses.


    # SMA 50:

    line(x, sma50, color='#D95F02', x_axis_type='datetime')

    # Bollinger shading glyph:

    bandprice = stackify(upperband, lowerband)  # Reverse the upper band data and append it to the lower band data.

    banddates = stackify(dates, dates)  # Do the same for the dates.

    # TODO: Explain how Patch works, and why the data has to be manipulated in this manner.

    patch(pandas.to_datetime(banddates), bandprice, color='#7570B3', fill_alpha=0.2, x_axis_type='datetime')


    # Remove hold, allow for more plots to be added.

    curplot().title = symbol
    curplot().height = 600
    curplot().width = 800

    yaxis().axis_label = 'Price (USD)'

    grid().grid_line_alpha = 0.4

    save(file_name)

    shutil.copy(file_name, 'templates')

    os.remove(file_name)


