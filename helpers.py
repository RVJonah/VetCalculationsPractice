import urllib.parse

from flask import redirect, render_template, request, session, jsonify, current_app
from functools import wraps

def apology(message, code=400):
    #Render message as an apology to user.
    def escape(s):

        # escapes special characters
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):

    # creates login required routes
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get(["user_id"]) is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def ssl_required(fn):

    #creates SSL only routes
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if current_app.config.get("SSL"):
            if request.is_secure:
                return fn(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))
        return fn(*args, **kwargs)
    return decorated_view