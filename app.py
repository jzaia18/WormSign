import psycopg2 as psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import example_util
import os, json
import datetime;

from utils.config import config

app = Flask(__name__)
DIR = os.path.dirname(__file__) or '.'
app.secret_key = os.urandom(16)


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn


def insert_user(username, password):
    """ insert a new user into the users table """
    checksql = """SELECT * FROM "Users" WHERE "Username" = '{}';""".format(username)
    sql = """INSERT INTO "Users"("Username", "Password", "DateJoined", "LastAccessDate") VALUES(%s, %s, %s, %s)"""
    ct = datetime.datetime.utcnow()
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(checksql)
        user = cur.fetchone()

        if user is not None:
            return 'failed'
        else:
            # execute the INSERT statement
            cur.execute(sql, (username, password, ct, ct))
            # commit the changes to the database
            conn.commit()

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 'success'


def login_user(username, password):
    """ logs user into the recipe manager """
    checksql = """SELECT * FROM "Users" WHERE "Username" = '{}' AND "Password" = '{}';""".format(username, password)
    ct = datetime.datetime.utcnow()
    sql = """UPDATE "Users" SET "LastAccessDate" = '{}' WHERE "Username" = '{}' AND "Password" = '{}'""".format(ct, username, password)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # check if user exists
        cur.execute(checksql)
        user = cur.fetchone()

        # if user is empty this login failed
        if user is None:
            return 'failed'
        else:
            # execute the UPDATE statement
            cur.execute(sql)
            # commit the changes to the database
            conn.commit()

        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return 'success'

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
