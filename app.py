from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from utils import example_util
import os, json

from utils.config import config
from utils.login import insert_user, login_user
from utils.search_recipe import search_recipe
from utils.search_ingredient import search_ingredient
from utils.create_recipe import create_recipe
from utils.create_category import create_category

app = Flask(__name__)
DIR = os.path.dirname(__file__) or '.'
app.secret_key = os.urandom(16)

DIFFICULTIES = ['Easy', 'Easy-Medium', 'Medium', 'Medium-Hard', 'Hard', 'Very-Hard']

def require_login(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'user' not in session or not session.get('user') or \
           'id' not in session or not session.get('id'):
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


@app.route("/createrecipe", methods=['GET', 'POST'])
@require_login
def create_recipe_route():
    if request.method == 'POST':
        recipe_name = request.form['RecipeName']
        description = request.form['Description']
        cook_time = int(request.form['CookTime'])
        servings = int(request.form['Servings'])
        difficulty = DIFFICULTIES[int(request.form['Difficulty'])]
        ingredient_list = json.loads(request.form['Ingredients'])
        print(ingredient_list)
        steps = request.form['Steps']
        results = create_recipe(recipe_name, description, cook_time, servings, difficulty, ingredient_list, steps, session['id'])
        print(results)
        return redirect(url_for('home'))
    return render_template("create_recipe.html", user=session.get('user'))


@app.route("/ingredientsearch", methods=['POST'])
def ingredient_search():
    if 'ingredient_name' not in request.form or not request.form['ingredient_name']:
        return json.dumps({})
    return json.dumps(search_ingredient(request.form['ingredient_name']))


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
@require_login
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


@app.route("/make_category", methods=['GET','POST'])
@require_login
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
