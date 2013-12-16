from flask import Flask, render_template
import datetime
import stockscopy

app = Flask(__name__)


# Define and add a home page.

@app.route('/')  # The base URL for the home page.
def resume():
    return render_template('resume.html')


@app.route('/echo/<message>')
def echo(message):
    # Echos the message passed to it.
    return "%s" % message


# Shameful, shameful plotting logic. This does NOT belong here. FIXME!

start = datetime.date(2012, 1, 1)

end = datetime.date.today()

periods = 50

# {% endshame %}

@app.route('/stocks/<symbol>')
def stocks(symbol):

    stockscopy.build_plot(symbol, periods, start, end)

    return render_template('%s.html' % symbol)

# Create plot HTML pages.

# Run this thing!
if __name__ == '__main__':
    app.run(debug=True)