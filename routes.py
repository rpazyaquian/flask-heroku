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

    s = request.args.get('symbol')

    print "testing for length of symbol array..."

    try:
        len(s)
    except TypeError:
        return render_template('stocks.html',
                               error='Please request a stock symbol.',
                               s_length=0,
                               sd_length=0)

    if len(s) == 0:
        return render_template('stocks.html',
                               error='Please request a stock symbol.',
                               s_length=0,
                               sd_length=0)

    symbols_list = s.split(',')

    snippet_dict = {}

    print "building plots..."
    for i in symbols_list:
        try:
            snippet_dict[i] = plots.build_plot(i.upper())
        except IOError:
            print "symbol %s not found" % i
            continue

    print "rendering template..."

    if len(snippet_dict) == 0:
        return render_template('stocks.html',
                               error='No valid symbols found.',
                               s_length=0,
                               sd_length=0)

    return render_template('stocks.html',
                           snippet_dict=snippet_dict,
                           sd_length=len(snippet_dict))

# Run this thing!
if __name__ == '__main__':
    app.run(debug=True)