from flask import Flask, render_template
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


@app.route('/stocks/<symbol>')
def lookup(symbol):

    snippet = plots.build_plot(symbol)

    return render_template('stocks.html',
                           snippet=snippet)


# Run this thing!
if __name__ == '__main__':
    app.run(debug=True)