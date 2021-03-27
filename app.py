import psycopg2 as psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import example_util
import os, json

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


#This is needed if we want to force user logins, leaving commented out for now

def require_login(f):
    #@wraps(f)
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

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('about'))
    return render_template("login.html")

if __name__ == '__main__':
    connection = connect()
    app.run(host='localhost', port=8080, debug=True)
