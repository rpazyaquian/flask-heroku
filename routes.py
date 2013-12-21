from flask import Flask, render_template, request
import plots

app = Flask(__name__)


# Define and add a home page.

@app.route('/')  # The base URL for the home page.
def resume():
    return render_template('resume.html')


@app.route('/echo/<message>')
def echo(message):
    # Echos the message passed to it.
    return "%s" % message


@app.route('/stocks')
def lookup():
    symbol = request.args.get('symbol')

    try:
        len(symbol)
    except TypeError:
        return render_template('stocks.html',
                               error='Please request a stock symbol.')

    try:
        snippet = plots.build_plot(symbol)
    except IOError:
        return render_template('stocks.html',
                               error='Symbol not found.')

    return render_template('stocks.html',
                           snippet=snippet)


# Run this thing!
if __name__ == '__main__':
    app.run(debug=True)