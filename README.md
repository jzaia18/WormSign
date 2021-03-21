# WormSign
Principles of Database Management project group


## Installing Flask
This project depends on Flask, which is a python library that allows you to create web servers.

Flask is available through [pip](https://pypi.org/project/pip/).
You can install it via command line by running `pip3 install flask`
Make sure to use pip3 instead of pip, as we are using python3

## Running the app
Once flask is installed you can easily run the app by running the main file app.py from the root of the repository: `python3 app.py`

It should print the following in your terminal:
```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 109-366-067
```
You can now open a web browser to https://localhost:8080 and should see the example app. Any changes you make to the app should show after refreshing the page. You won't need to rerun app.py unless you save code that terminates the app; this is a setting that I've turned on called debug mode. But you may have to hard refresh your browser with ctrl+shift+R to clear cached content when modifying certain files.

## Layout of the code

There are 3 folders critical to the app:

utils/ contains python code that can be used to assist the app, this is important for keeping the main app file clean. Ideally app.py should only contain code for routing the Flask app (choosing which routes execute what code). All other code (including db calls) should go in utils and be called from app.py.

templates/ contains html templates that get rendered by Flask. The files don't have to contain strictly html, they use jinja2 which allows for embedding small bits of python code within the html itself, as well as "extending" other html files. Thus, we have a base.html that holds code we need for *every* file and have the other files "extend" it to prevent duplicating code.

static/ hosts static files, files that are not serverside code and are not prone to frequent change. This generally just means images, css, and js files.
