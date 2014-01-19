from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_user, current_user
from forms import RegistrationForm, LoginForm


import plots
import logging
from logging import StreamHandler

app = Flask(__name__)
app.secret_key = 'what_the_hell_is_this_used_for'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(16))
    search = db.Column(db.String(500))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


#def flash_errors(form):
#    for field, errors in form.errors.items():
#        for error in errors:
#            flash(u"Error in %s field - %s" % (
#                getattr(form, field).label.text,
#                error
#            ))

file_handler = StreamHandler()
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/')
def resume():
    return render_template('resume.html')


@app.route('/echo/<path:message>')
def echo(message):
    return "%s" % message


@app.route('/stocks')
def lookup():
    s = request.args.get('symbol')

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

    for i in symbols_list:
        try:
            snippet_dict[i] = plots.build_plot(i.upper())
        except IOError:
            print "symbol %s not found" % i
            continue

    if len(snippet_dict) == 0:
        return render_template('stocks.html',
                               error='No valid symbols found.',
                               s_length=0,
                               sd_length=0)

    return render_template('stocks.html',
                           snippet_dict=snippet_dict,
                           sd_length=len(snippet_dict))


@app.route('/stocks/<path:user>')
def user_lookup(user):
    s = User.query.filter_by(username=user).first().stored_search

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

    for i in symbols_list:
        try:
            snippet_dict[i] = plots.build_plot(i.upper())
        except IOError:
            print "symbol %s not found" % i
            continue

    if len(snippet_dict) == 0:
        return render_template('stocks.html',
                               error='No valid symbols found.',
                               s_length=0,
                               sd_length=0)

    return render_template('stocks.html',
                           snippet_dict=snippet_dict,
                           sd_length=len(snippet_dict))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('lookup'))
    else:
        flash_errors(form)

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        login_user(g.user, remember=True)
        flash('Login successful.')
        return redirect(url_for('lookup'))
    return render_template('login.html', form=form)


# Run this thing!
if __name__ == '__main__':
    app.run(debug=True)