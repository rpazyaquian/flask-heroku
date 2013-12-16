__author__ = 'rebecca'

from bokeh.plotting import *

import datetime
import pandas
import pandas.io.data as web
from pyta import *

# Example of computing Bollinger bands for several stock charts at once.
# This is achieved by using the Patch glyph.
# Uses Pandas to access financial data, but converts most of the data to Numpy arrays.
# Maybe this can be simplified?
# Any other critique is well appreciated.


# Declare output file.

output_file('stocks.html', title='How are my stocks doing today?')

# Define timespan.

start = datetime.date(2012, 1, 1)

end = datetime.date.today()

# Define time periods (for SMA and Bollinger).

periods = 50

# List of symbols to look up.

symbols = ['AAPL', 'GOOG', 'MSFT', 'NTDOY']


# Create a plot for each symbol.

for s in symbols:

    # Obtain the data.

    data = web.DataReader(s, 'google', start, end)

    close = data['Close'].values  # Returns Numpy array.

    dates = data.index.values  # Returns Numpy array.


    # Plot raw stock data.

    x = data.index

    y = close

    line(x[50:], y[50:], color='#1B9E77', x_axis_type='datetime')
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

    curplot().title = s
    curplot().height = 600
    curplot().width = 800

    #curplot().create_html_snippet()

    yaxis().axis_label = 'Price (USD)'

    grid().grid_line_alpha = 0.4

    hold()


# Finally, display all plots.

show()