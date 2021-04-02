from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from utils import example_util
import os, json

from utils.category_help import *
from utils.config import config
from utils.login import insert_user, login_user
from utils.search_ingredient import search_ingredient
from utils.create_recipe import *
from utils.search_recipe import *
from utils.create_category import create_category
from utils.show_pantry import show_pantry, add_to_pantry, update_pantry
from utils.clean_strings import clean_string

app = Flask(__name__)
DIR = os.path.dirname(__file__) or '.'
app.secret_key = os.urandom(16)

DIFFICULTIES = [None, 'Easy', 'Easy-Medium', 'Medium', 'Medium-Hard', 'Hard', 'Very-Hard']

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
        steps = clean_steps(request.form['Steps'])
        if 'RecipeId' in request.form:
            recipe_id = request.form['RecipeId']
            results = update_recipe(recipe_id, recipe_name, description, cook_time, servings, difficulty, ingredient_list, steps)
        else:
            results = create_recipe(recipe_name, description, cook_time, servings, difficulty, ingredient_list, steps, session['id'])

        if not results:
            flash("There was an error creating this recipe.")
        return redirect(url_for('home'))
    return render_template("create_recipe.html")


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
        sortType = request.form['sortType']
        keyword = request.form['keyword']
        userid = session['id']
        # results from searching the db
        if sortType == 'alpha':
            results = search_recipe(searchType, keyword, userid)
        elif sortType == 'rating':
            results = search_recipe_rating(searchType, keyword, userid)
        else:
            results = search_recipe_recent(searchType, keyword, userid)
        # checks to see if there was at least one result
        if len(results) == 0:
            notfound = 'No recipes found'
    return render_template("home.html", results=results, notfound=notfound, keyword=keyword)


@app.route("/recipe")
def display_recipe():
    recipeid = request.args.get('id')
    recipe = get_recipe(recipeid)
    rating = get_rating(recipe[0])
    creator = get_creator(recipe[7])
    ingredients = get_ingredients(recipeid)
    steps = format_steps(recipe[6])
    return render_template("recipe.html", recipe=recipe, creator=creator,
                           ingredients=ingredients, steps=steps, rating=rating)


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


@app.route("/editrecipe")
@require_login
def edit_recipe():
    recipe_id = request.args.get('id')
    recipe = get_recipe(recipe_id)

    recipe_name = recipe[1]
    description = recipe[2]
    servings = recipe[3]
    cook_time = recipe[4]
    difficulty = {'Easy': 1, 'Easy-Medium': 2, 'Medium': 3, 'Medium-Hard': 4, 'Hard': 5}[recipe[5]]
    ingredients = get_ingredients_with_ids(recipe_id)
    steps = clean_string(recipe[6])
    return render_template("create_recipe.html", recipe_id=recipe_id, recipe_name=recipe_name, description=description, servings=servings, cook_time=cook_time, difficulty=difficulty, ingredients=ingredients, steps=steps)


@app.route("/deleterecipe")
@require_login
def delete_recipe():
    recipe_id = request.args.get('id')
    success = remove_recipe(recipe_id)
    if not success:
        flash("Cannot remove this recipe. NOTE: Cooked Recipes cannot be removed.")
    return redirect(url_for('my_recipes'))


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



@app.route("/addcategory")
def add_category():
    recipeid = request.args.get('id')
    categories = get_categories(session['id'])
    return render_template("add_category.html", recipeid=recipeid, categories=categories)


@app.route("/processcategory", methods=['GET', 'POST'])
def process_category():
    recipeid = request.args.get('id')
    recipe = get_recipe(recipeid)
    rating = get_rating(recipe[0])
    creator = get_creator(recipe[7])
    ingredients = get_ingredients(recipeid)
    steps = format_steps(recipe[6])
    categoryid = request.form.get('category', False)
    error = insert_category(recipeid, categoryid)
    if error == 'failed':
        message = "This recipe already belongs to that category"
    elif error == 'failed2':
        message = "You did not select a category"
    else:
        message = "Recipe has been added to category"
    return render_template("recipe.html", recipe=recipe, creator=creator,
                           ingredients=ingredients, steps=steps, rating=rating, message=message)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
