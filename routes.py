from flask import Flask, render_template

app = Flask(__name__)


# Define and add a home page.

@app.route('/')  # The base URL for the home page.
def resume():
    return render_template('resume.html')


#@app.route('/stocks/')
#def stocks():
#    return render_template('stocks.html')


# Run this thing!
if __name__ == '__main__':
    app.run(debug=True)