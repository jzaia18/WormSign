from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils import example_util
import os, json

app = Flask(__name__)
DIR = os.path.dirname(__file__) or '.'
app.secret_key = os.urandom(16)

'''
This is needed if we want to force user logins, leaving commented out for now

def require_login(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in')
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)
    return inner
'''

@app.route("/")
def root():
    return render_template("home.html")

@app.route("/home")
def about():
    return render_template("home.html", test=example_util.example_fxn())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
