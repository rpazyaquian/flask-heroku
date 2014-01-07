__author__ = 'rebecca'

from bokeh.plotting import *
from bokeh.objects import Range1d

import pandas
import pandas.io.data as web
from pyta import *
import numpy as np


#Trying to add signals to the indicators.
def sma_signal(sma50, sma200):
    output_array = []
    for i in range(len(sma50)):
        if i == 0:
            output_array.append('BEGIN')
            continue
        if pandas.isnull(sma50[i]):
            output_array.append('WAIT')
        elif sma50[i] > sma200[i]:
            if sma50[i-1] < sma200[i-1]:
                output_array.append('BUY')
            else:
                output_array.append('WAIT')
        elif sma50[i] < sma200[i]:
            if sma50[i-1] > sma200[i-1]:
                output_array.append('SELL')
            else:
                output_array.append('WAIT')
        else:
            output_array.append('WAIT')
    return output_array

# Create a plot for each symbol.

def build_data(symbol):
    periods = 50
    data = web.DataReader(symbol, 'google')
    close = data['Close']

    sma50 = sma(close, periods)
    data['SMA50'] = sma50

    sma200 = sma(close, 200)
    data['SMA200'] = sma200

    upperband = bollinger_upper(close, sma50, periods)
    lowerband = bollinger_lower(close, sma50, periods)
    data['Bollinger (upper)'] = upperband
    data['Bollinger (lower)'] = lowerband

    rsi50 = rsi(close)
    data['RSI50'] = rsi50

    macd = macd_line(close)
    signal = macd_signal(macd)
    hist = macd_hist(macd, signal)

    data['MACD Line'] = macd
    data['MACD Signal'] = signal
    data['MACD Histogram'] = hist

    return data



def build_plot(symbol):

    data = build_data(symbol)

    # Generate data.
    file_name = '%s.html' % symbol
    output_file(file_name,
                title='How are my stocks doing today?')

    close = data['Close']
    dates = data.index

    # Define plot constants.

    plot_width = 1000

    # Perform TA on stock data.
    # TODO: Make the buy/sell signals actually do something.

    # Define SMA 50/200.
    sma50 = data['SMA50']
    sma200 = data['SMA200']

    # Define Bollinger Bands.
    upperband = data['Bollinger (upper)']
    lowerband = data['Bollinger (lower)']

    # Define RSI.
    rsi50 = data['RSI50']  # TODO: Figure out a way to translate "crosses under/above line" to a sell signal.


    # Define MACD Line, Signal, and Histogram.
    macd = data['MACD Line']
    signal = data['MACD Signal']  # TODO: Actually use these. Figure out subplots!
    hist = data['MACD Histogram']


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
         color='#4daf4a')

    line(x, (np.ones(len(rsi50)) * 70),
         color='#e41a1c')

    # Miscellaneous plot attributes.

    rsi_plot.title = symbol
    rsi_plot.height = 200
    rsi_plot.width = plot_width
    rsi_plot.min_border_bottom = 10
    grid().grid_line_alpha = 0.4
    yaxis().axis_label = 'RSI'

    # Remove hold for the main plot.
    hold()

    # Plot raw stock data.
    main_plot = line(x, y,
                     color='#1B9E77',
                     legend='Price at Close',
                     x_axis_type=None,
                     title='')

    # Hold for the overlays.
    hold()

    # Plot overlays.

    # SMA 50:
    line(x, sma50,
         color='#D95F02',
         legend='50-day SMA')

    # SMA 200:
    line(x, sma200,
         color='#e7298a',
         legend='200-day SMA')

    # Bollinger shading glyph:
    bandprice = stackify(upperband, lowerband)  # Reverse the upper band data and append it to the lower band data.
    banddates = stackify(dates, dates)  # Do the same for the dates.
    patch(pandas.to_datetime(banddates), bandprice,
          color='#7570B3',
          fill_alpha=0.2)

    # Remove hold, allow for more plots to be added.
    hold()

    # Miscellaneous plot attributes.
    main_plot.height = 400
    main_plot.width = plot_width
    yaxis().axis_label = 'Price (USD)'
    grid().grid_line_alpha = 0.4

    xaxis().bounds = xbounds
    curplot().x_range = x_range

    # Plot MACD.

    macd_plot = line(x, macd,
         color='#D95F02',
         title='',
         x_axis_type='datetime')

    hold()

    line(x, signal,
         color='#1B9E77')

    hold()

    # Attributes.
    macd_plot.height = 200
    macd_plot.width = plot_width
    yaxis().axis_label = 'MACD'

    macd_plot.min_border_top = 0
    macd_plot.min_border_bottom = 100

    # Make a grid and snippet from this.

    plot_grid = gridplot([[rsi_plot], [main_plot], [macd_plot]])

    snippet = plot_grid.create_html_snippet(embed_base_url='../static/js/',
                                            embed_save_loc='./static/js')

    # Return signal arrays.

    sma_signals = sma_signal(sma50, sma200)

    return snippet