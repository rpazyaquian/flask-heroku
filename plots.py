__author__ = 'rebecca'

from bokeh.plotting import *
from bokeh.objects import Range1d

import pandas
import pandas.io.data as web
from pyta import *
import numpy as np


# Create a plot for each symbol.

def build_plot(symbol):
    periods = 50
    file_name = '%s.html' % symbol
    output_file(file_name,
                title='How are my stocks doing today?')
    data = web.DataReader(symbol, 'google')
    close = data['Close'].values  # Returns Numpy array.
    dates = data.index.values  # Returns Numpy array.


    # Perform TA on stock data.
    # TODO: Make the buy/sell signals actually do something.

    # Define SMA 50.
    sma50 = sma(close, periods)

    # Define Bollinger Bands.
    upperband = bollinger_upper(close, sma50, periods)
    lowerband = bollinger_lower(close, sma50, periods)

    # Define RSI.
    rsi50 = rsi(close)  # TODO: Figure out a way to translate "crosses under/above line" to a sell signal.

    # Define MACD Line, Signal, and Histogram.
    macd = macd_line(close)
    signal = macd_signal(close)  # TODO: Actually use these. Figure out subplots!
    hist = macd_hist(close)


    # Finished with the data? Then it's time to plot!

    x = data.index
    y = close

    # Plot RSI (remember, it goes on top)

    rsi_plot = line(x[50:], rsi50,
                    color='#000000',
                    x_axis_type=None)

    curplot().title = symbol
    curplot().height = 200
    curplot().width = 800
    grid().grid_line_alpha = 0.4
    yaxis().axis_label = 'RSI'

    # Define RSI axis boundaries.
    curplot().y_range = Range1d(start=0, end=100)
    yaxis().bounds = [0, 100]

    xbounds = [x[50], x[-1]]
    xrange = Range1d(start=x[50], end=x[-1])

    xaxis().bounds = xbounds
    curplot().x_range = xrange

    hold()

    rsi_plot = line(x[50:], rsi50,
                    color='#000000',
                    x_axis_type=None, )

    rsi_min = line(x[50:], (np.ones(len(rsi50)) * 30),
                   color='#00FF00')

    rsi_max = line(x[50:], (np.ones(len(rsi50)) * 70),
                   color='#00FF00')

    hold()

    # Plot raw stock data.
    main_plot = line(x[50:], y[50:],
                     color='#1B9E77',
                     legend='Price at Close',
                     x_axis_type = 'datetime',
                     title='')

    # Hold for the overlays.
    hold()

    # Plot overlays.

    # SMA 50:
    line(x, sma50,
         color='#D95F02',
         legend='50-day SMA')

    # Bollinger shading glyph:
    bandprice = stackify(upperband, lowerband)  # Reverse the upper band data and append it to the lower band data.
    banddates = stackify(dates, dates)  # Do the same for the dates.
    patch(pandas.to_datetime(banddates), bandprice,
          color='#7570B3',
          fill_alpha=0.2)

    # Remove hold, allow for more plots to be added.
    hold()

    # Miscellaneous plot attributes.
    curplot().height = 600
    curplot().width = 800
    yaxis().axis_label = 'Price (USD)'
    grid().grid_line_alpha = 0.4

    xaxis().bounds = xbounds
    curplot().x_range = xrange

    main_plot.min_border_top = 0

    # Make a grid and snippet from this.

    plot_grid = gridplot([[rsi_plot], [main_plot]])

    snippet = plot_grid.create_html_snippet(embed_base_url='../static/js/',
                                            embed_save_loc='./static/js')

    return snippet