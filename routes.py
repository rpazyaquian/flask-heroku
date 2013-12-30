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


@app.route('/stocks')
def homestock():

    return render_template('stocks.html')

# TODO: Which of these two approaches is better?

@app.route('/stocks/<symbol>')
def lookup(symbol):
    s = symbol

    try:
        len(s)
    except TypeError:
        return render_template('stocks.html',
                               error='Please request a stock symbol.')

    snippet_list = []

    for i in s.split(','):

        try:
            snippet_list.append(plots.build_plot(i, days_ago=50))
        except IOError:
            return render_template('stocks.html',
                                   error='One or more symbols were not found.')

    return render_template('stocks.html',
                           snippet_list=snippet_list)


#@app.route('/stocks')
#def lookup():
#    s = request.args.get('symbol')
#
#    try:
#        len(s)
#    except TypeError:
#        return render_template('stocks.html',
#                               error='Please request a stock symbol.')
#
#    snippet_list = []
#
#    for i in s.split(','):
#
#        try:
#            snippet_list.append(plots.build_plot(i))
#        except IOError:
#            return render_template('stocks.html',
#                                   error='One or more symbols were not found.')
#
#    return render_template('stocks.html',
#                           snippet_list=snippet_list)

# Run this thing!
if __name__ == '__main__':
    app.run(debug=True)