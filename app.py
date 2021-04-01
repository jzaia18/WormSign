from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from utils import example_util
import os, json

from utils.config import config
from utils.login import insert_user, login_user
from utils.search_recipe import search_recipe
from utils.create_category import create_category
from utils.show_pantry import show_pantry, update_pantry

app = Flask(__name__)
DIR = os.path.dirname(__file__) or '.'
app.secret_key = os.urandom(16)


def require_login(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)

    return inner


@app.route("/")
@require_login
def root():
    return redirect(url_for("home"))


@app.route("/home")
@require_login
def home():
    return render_template("home.html", test=example_util.example_fxn())


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_result, user_id = login_user(username, password)
        if login_result == 'no-account':
            error = 'Account with that Username does not exist'
        elif login_result == 'failed':
            error = 'Incorrect Password'
        else:
            flash('Successfully logged in')
            session['user'] = username
            session['id'] = user_id
            return redirect(url_for('home'))
    return render_template("login.html", error=error)


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        insert_result, user_id = insert_user(username, password)
        if insert_result == 'failed':
            error = 'This Username already exists, please try another'
        else:
            flash('Account successfully created!')
            session['user'] = username
            session['id'] = user_id
            return redirect(url_for('home'))
    return render_template("create_account.html", error=error)


@app.route("/findrecipes", methods=['POST'])
def find_recipe():
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


@app.route("/showpantry", methods=['GET', 'POST'])
def showpantry():
    uid = session['id']
    noResults = None
    error = None
    if request.method == 'POST':
        # results from searching the db
        ingredient = request.form['pantry_order']
        amount = request.form['amount']
        purchased = request.form['buy_date']
        expires = request.form['exp_date']

        error = update_pantry(ingredient, amount, purchased, expires, uid)  # update with form info

    results = show_pantry(uid)
    # checks to see if there was at least one result
    if len(results) == 0:
        noResults = 'No Pantry Data!'
    return render_template("manage_pantry.html", results=results, noResults=noResults, uid=uid, error=error)


@app.route("/make_category", methods=['GET', 'POST'])
def make_category():
    error = None
    if request.method == 'POST':
        category_name = request.form['category_name']
        create_category_result = create_category(session['id'], category_name)
        if create_category_result == 'failed':
            error = 'You already have a category with this name, please try another'
        else:
            flash('Category successfully created!')
            return redirect(url_for('home'))

    return render_template("make_category.html", error=error)

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
