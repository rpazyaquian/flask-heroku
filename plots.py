__author__ = 'rebecca'

from bokeh.plotting import *
from bokeh.objects import Range1d

import pandas
import pandas.io.data as web
from pyta import *
import numpy as np


# Create a plot for each symbol.

def build_plot(symbol):

    # Generate data.
    periods = 50
    file_name = '%s.html' % symbol
    output_file(file_name,
                title='How are my stocks doing today?')
    data = web.DataReader(symbol, 'google')
    close = data['Close'].values  # Returns Numpy array.
    dates = data.index.values  # Returns Numpy array.

    # Define plot constants.

    plot_width = 1000

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

    # Predefine plot for axis buggery.

    rsi_plot = line(x, rsi50,
                    color='#000000',
                    x_axis_type=None)

    # Define RSI axis boundaries.
    x_range = Range1d(start=x[0], end=x[-1])
    xbounds = [x[0], x[-1]]

    curplot().y_range = Range1d(start=0, end=100)
    curplot().x_range = x_range

    yaxis().bounds = [0, 100]
    xaxis().bounds = xbounds

    hold()

    rsi_plot = line(x, rsi50,
                    color='#000000',
                    x_axis_type=None)

    line(x, (np.ones(len(rsi50)) * 30),
         color='#00FF00')

    line(x, (np.ones(len(rsi50)) * 70),
         color='#FF0000')

    rsi_plot.title = symbol
    rsi_plot.height = 200
    rsi_plot.width = plot_width
    grid().grid_line_alpha = 0.4
    yaxis().axis_label = 'RSI'

    # Remove hold for the main plot.
    hold()

    # Plot raw stock data.
    main_plot = line(x, y,
                     color='#1B9E77',
                     legend='Price at Close',
                     x_axis_type='datetime',
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
    main_plot.height = 600
    main_plot.width = plot_width
    yaxis().axis_label = 'Price (USD)'
    grid().grid_line_alpha = 0.4

    xaxis().bounds = xbounds
    curplot().x_range = x_range

    main_plot.min_border_top = 0
    main_plot.min_border_bottom = 100

    # Make a grid and snippet from this.

    plot_grid = gridplot([[rsi_plot], [main_plot]])

    snippet = plot_grid.create_html_snippet(embed_base_url='../static/js/',
                                            embed_save_loc='./static/js')

    return snippet