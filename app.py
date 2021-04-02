from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from utils import example_util
import os, json

from utils.config import config
from utils.login import insert_user, login_user
from utils.search_recipe import search_recipe
from utils.search_ingredient import search_ingredient
from utils.create_recipe import create_recipe, get_my_recipes
from utils.create_category import create_category
from utils.show_pantry import show_pantry, add_to_pantry, update_pantry

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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_result, user_id = login_user(username, password)
        if login_result == 'no-account':
            flash('Account with that Username does not exist')
        elif login_result == 'failed':
            flash('Incorrect Password')
        else:
            flash('Successfully logged in')
            session['user'] = username
            session['id'] = user_id
            return redirect(url_for('home'))
    return render_template("login.html")

@app.route("/signout")
@require_login
def signout():
    session.clear()
    flash("Successfully logged out")
    return redirect(url_for('login'))


@app.route("/create_account", methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        insert_result, user_id = insert_user(username, password)
        if insert_result == 'failed':
            flash('This Username already exists, please try another')
        else:
            flash('Account successfully created!')
            session['user'] = username
            session['id'] = user_id
            return redirect(url_for('home'))
    return render_template("create_account.html")


@app.route("/myrecipes")
@require_login
def my_recipes():
    results = get_my_recipes(session['id'])
    if results is None:
        flash("ERROR: Unable to get recipes for user " + session['user'])
    return render_template("my_recipes.html", recipes=results)

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
        steps = request.form['Steps']
        results = create_recipe(recipe_name, description, cook_time, servings, difficulty, ingredient_list, steps, session['id'])
        #print(results)
        return redirect(url_for('home'))
    return render_template("create_recipe.html", user=session.get('user'))


@app.route("/ingredientsearch", methods=['POST'])
def ingredient_search():
    if 'ingredient_name' not in request.form or not request.form['ingredient_name']:
        return json.dumps({})
    return json.dumps(search_ingredient(request.form['ingredient_name']))


@app.route("/findrecipes", methods=['POST'])
@require_login
def find_recipe():
    notfound = None
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
@require_login
def showpantry():       # handles when a user adds to their pantry
    uid = session['id']
    noResults = None
    if request.method == 'POST':
        # results from searching the db
        ingredient = request.form['pantry_order']
        amount = request.form['amount']
        purchased = request.form['buy_date']
        expires = request.form['exp_date']

        error = add_to_pantry(ingredient, amount, purchased, expires, uid)  # update with form info

        if error:
            flash(error)

    results = show_pantry(uid)  # always want to load pantry table
    # checks to see if there was at least one result
    if len(results) == 0:
        noResults = 'No Pantry Data!'
    return render_template("manage_pantry.html", results=results, noResults=noResults, uid=uid)


@app.route("/updatepantry", methods=['POST'])  # for when a user updates an order within their pantry
@require_login
def updatepantry():
    uid = session['id']
    noResults = None
    if request.method == 'POST':
        # results from searching the db
        order_id = request.form['update_order']
        amount = request.form['new_amount']

        error = update_pantry(order_id, amount, uid)  # update with form info
        if error:
            flash(error)
    return redirect(url_for('showpantry'))


@app.route("/make_category", methods=['GET', 'POST'])
@require_login
def make_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        create_category_result = create_category(session['id'], category_name)
        if create_category_result == 'failed':
            flash('You already have a category with this name, please try another')
        else:
            flash('Category successfully created!')
            return redirect(url_for('home'))

    return render_template("make_category.html")


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
