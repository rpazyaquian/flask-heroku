from flask import Flask, render_template

app = Flask(__name__)


# Define and add a home page.

@app.route('/')  # The base URL for the home page.
def home():  # What is a homepage?
    return render_template('home.html')  # It is a rendering of home.html.


# Unsemantic testing.

@app.route('/gridtest')
def about():
    return render_template('gridtest.html')


# Trial projects page.

@app.route('/projects')
def projects():
    return render_template('projects.html')

# Run this thing!
if __name__ == '__main__':
    app.run(debug=True)