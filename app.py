from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import example_util
import os, json

from utils.config import config
from utils.login import insert_user, login_user

app = Flask(__name__)
DIR = os.path.dirname(__file__) or '.'
app.secret_key = os.urandom(16)


def require_login(f):
    # @wraps(f)
    def inner(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in')
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)

    return inner


@app.route("/")
@require_login
def root():
    return render_template("home.html")


@app.route("/home")
def about():
    return render_template("home.html", test=example_util.example_fxn())


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        loginresult = login_user(username, password)
        if loginresult == 'failed':
            error = 'Incorrect Username and Password'
        else:
            flash('Successfully logged in')
            return redirect(url_for('about'))
    return render_template("login.html", error=error)


@app.route("/createaccount", methods=['GET', 'POST'])
def createaccount():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        insertresult = insert_user(username, password)
        if insertresult == 'failed':
            error = 'This Username already exists, please try another'
        else:
            flash('Account successfully created!')
            return redirect(url_for('about'))
    return render_template("createaccount.html", error=error)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
