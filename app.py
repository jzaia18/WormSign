from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import example_util
import os, json

from utils.config import config
from utils.login import insert_user, login_user
from utils.search_recipe import search_recipe

app = Flask(__name__)
DIR = os.path.dirname(__file__) or '.'
app.secret_key = os.urandom(16)


def require_login(f):
    # @wraps(f)
    def inner(*args, **kwargs):
        if 'user' not in session:
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
        if loginresult == 'no-account':
            error = 'Account with that Username does not exist'
        elif loginresult == 'failed':
            error = 'Incorrect Password'
        else:
            flash('Successfully logged in')
            return redirect(url_for('about'))
    return render_template("login.html", error=error)


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
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
    return render_template("create_account.html", error=error)


@app.route("/findrecipes", methods=['GET', 'POST'])
def findrecipe():
    notfound = None
    error = None
    if request.method == 'POST':
        # what the user entered
        searchType = request.form['searchType']
        keyword = request.form['keyword']
        # results from searching the db
        results = search_recipe(searchType, keyword)
        # checks to see if there was at least one result
        if len(results) == 0:
            notfound = 'No recipes found'
    return render_template("home.html", results=results, notfound=notfound, keyword=keyword)

@app.route("/managepantry", methods=['GET', 'POST'])
def managepantry():
    notfound = None
    error = None
    # if request.method == 'POST':
        # what the user entered
        # sortType = request.form['sortType']
        # keyword = request.form['keyword']
        # results from searching the db
        # results = search_recipe(sortType, keyword)
        # checks to see if there was at least one result
        # if len(results) == 0:
            # notfound = 'No recipes found'
    return render_template("home.html")


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
