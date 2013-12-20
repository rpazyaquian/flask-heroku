__author__ = 'rebecca'

from bokeh.plotting import *

import datetime
import pandas
import pandas.io.data as web
from pyta import *


# Create a plot for each symbol.

def build_plot(symbol):
    start = datetime.date(2011, 1, 1)
    end = datetime.date.today()
    periods = 50
    file_name = '%s.html' % symbol
    output_file(file_name,
                title='How are my stocks doing today?')
    data = web.DataReader(symbol, 'google', start, end)
    close = data['Close'].values  # Returns Numpy array.
    dates = data.index.values  # Returns Numpy array.

    # Plot raw stock data.
    x = data.index
    y = close
    line(x[50:], y[50:],
         color='#1B9E77',
         x_axis_type='datetime',
         legend='Price at Close')
    hold()


    # Perform TA on stock data.

    # Define SMA 50.
    sma50 = sma(close, periods)

    # Define Bollinger Bands.
    upperband = bollinger_upper(close, sma50, periods)
    lowerband = bollinger_lower(close, sma50, periods)

    # Define RSI.
    rsi50 = rsi(close)  # TODO: Figure out a way to translate "crosses under/above line" to a sell signal.

    # Define MACD Line, Signal, and Histogram.
    macd = macd_line(close)
    signal = macd_signal(close)
    hist = macd_hist(close)


    # Plot analyses.

    # SMA 50:
    line(x, sma50,
         color='#D95F02',
         x_axis_type='datetime',
         legend='50-day SMA')

    # Bollinger shading glyph:
    bandprice = stackify(upperband, lowerband)  # Reverse the upper band data and append it to the lower band data.
    banddates = stackify(dates, dates)  # Do the same for the dates.
    patch(pandas.to_datetime(banddates), bandprice,
          color='#7570B3',
          fill_alpha=0.2,
          x_axis_type='datetime')


    # Remove hold, allow for more plots to be added.
    curplot().title = symbol
    curplot().height = 600
    curplot().width = 1000

    yaxis().axis_label = 'Price (USD)'

    grid().grid_line_alpha = 0.4

    snippet = curplot().create_html_snippet(embed_base_url='../static/js/',
                                            embed_save_loc='./static/js')
    return snippet