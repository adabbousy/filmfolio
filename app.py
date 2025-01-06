from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import requests

app = Flask(__name__)

db = SQL("sqlite:///movies.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def contains_digit(password):
    return any(char.isdigit() for char in password)


def contains_lower(password):
    return any(char.islower() for char in password)


def contains_upper(password):
    return any(char.isupper() for char in password)


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        firstname = request.form.get("firstname").lower()
        lastname = request.form.get("lastname").lower()
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not firstname:
            return apology("Missing first name")

        if not lastname:
            return apology("Missing last name")

        if not username:
            return apology("Missing username")

        if len(username) < 3:
            return apology("Username too short")

        if not password:
            return apology("Missing password")

        if len(password) < 6:
            return apology("Password too short")

        if not contains_digit(password):
            return apology("Password must contain at least 1 digit")

        if not contains_lower(password):
            return apology("Password must contain at least 1 lowercase letter")

        if not contains_upper(password):
            return apology("Password must contain at least 1 uppercase letter")

        if not confirmation:
            return apology("Must confirm password")

        if password != confirmation:
            return apology("Confirm password correctly")

        hashed_pass = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users(username, firstname, lastname, hash) VALUES(?, ?, ?, ?)", username, firstname, lastname, hashed_pass)
            return render_template("login.html")
        except ValueError:
            return apology("Username already taken")


@app.route("/password", methods=["GET", "POST"])
def password():
    if request.method == "GET":
        return render_template("password.html")
    else:
        password = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["hash"]
        old = request.form.get("old")
        new = request.form.get("new")
        confirmation = request.form.get("confirmation")

        if not old or not new or not confirmation:
            return apology("Missing input")

        if not check_password_hash(password, old):
            return apology("Incorrect password")

        if len(new) < 6:
            return apology("Password too short")

        if not contains_digit(new):
            return apology("Password must contain at least 1 digit")

        if not contains_lower(new):
            return apology("Password must contain at least 1 lowercase letter")

        if not contains_upper(new):
            return apology("Password must contain at least 1 uppercase letter")

        if new != confirmation:
            return apology("Confirm password correctly")

        hashed_new = generate_password_hash(new)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_new, session["user_id"])

        return redirect("/login")


@app.route("/")
@login_required
def index():
    firstname = db.execute("SELECT firstname FROM users WHERE id = ?", session["user_id"])[0]["firstname"].title()
    lastname = db.execute("SELECT lastname FROM users WHERE id = ?", session["user_id"])[0]["lastname"].title()

    return render_template("index.html", firstname=firstname, lastname=lastname)


@app.route("/add-to-watchlist", methods=["POST"])
@login_required
def add_to_watchlist():
    data = request.get_json()
    movieId = data.get('movieId')
    title = data.get('title')
    overview = data.get('overview')
    poster_path = data.get('poster_path')
    release_date = data.get('release_date')
    vote_average = data.get('vote_average')
    if (len(db.execute("SELECT id FROM movies WHERE id = ?", movieId)) == 0):
        db.execute("INSERT INTO movies (id, title, overview, poster_path, release_date, vote_average) VALUES (?, ?, ?, ?, ?, ?)",
                movieId, title, overview, poster_path, release_date, vote_average)
    if (len(db.execute("SELECT * FROM watchlist WHERE movie_id = ? AND user_id = ?", movieId, session["user_id"])) == 0):
        db.execute("INSERT INTO watchlist (user_id, movie_id) VALUES (?, ?)", session["user_id"], movieId)
        db.execute("DELETE FROM watched WHERE user_id = ? AND movie_id = ?", session["user_id"], movieId)
    return



@app.route("/add-to-watched", methods=["POST"])
@login_required
def add_to_watched():
    data = request.get_json()
    movieId = data.get('movieId')
    title = data.get('title')
    overview = data.get('overview')
    poster_path = data.get('poster_path')
    release_date = data.get('release_date')
    vote_average = data.get('vote_average')
    if (len(db.execute("SELECT id FROM movies WHERE id = ?", movieId)) == 0):
        db.execute("INSERT INTO movies (id, title, overview, poster_path, release_date, vote_average) VALUES (?, ?, ?, ?, ?, ?)",
                movieId, title, overview, poster_path, release_date, vote_average)
    if (len(db.execute("SELECT * FROM watched WHERE movie_id = ? AND user_id = ?", movieId, session["user_id"])) == 0):
        db.execute("INSERT INTO watched (user_id, movie_id) VALUES (?, ?)", session["user_id"], movieId)
        db.execute("DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?", session["user_id"], movieId)
    return



@app.route("/watchlist")
@login_required
def watchlist():
    firstname = db.execute("SELECT firstname FROM users WHERE id = ?", session["user_id"])[0]["firstname"].title()
    lastname = db.execute("SELECT lastname FROM users WHERE id = ?", session["user_id"])[0]["lastname"].title()

    movies = db.execute("SELECT * FROM movies WHERE id IN (SELECT movie_id FROM watchlist WHERE user_id = ?) ORDER BY title", session["user_id"])
    return render_template("watchlist.html", firstname=firstname, lastname=lastname, movies=movies)


@app.route("/remove-from-watchlist", methods=["POST"])
@login_required
def remove_from_watchlist():
    data = request.get_json()
    movieId = data.get('movieId')
    db.execute("DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?",session["user_id"], movieId)
    return


@app.route("/remove-from-watched", methods=["POST"])
@login_required
def remove_from_watched():
    data = request.get_json()
    movieId = data.get('movieId')
    db.execute("DELETE FROM watched WHERE user_id = ? AND movie_id = ?", session["user_id"], movieId)


@app.route("/watched")
@login_required
def watched():
    firstname = db.execute("SELECT firstname FROM users WHERE id = ?", session["user_id"])[0]["firstname"].title()
    lastname = db.execute("SELECT lastname FROM users WHERE id = ?", session["user_id"])[0]["lastname"].title()

    movies = db.execute("SELECT * FROM movies WHERE id IN (SELECT movie_id FROM watched WHERE user_id = ?) ORDER BY title", session["user_id"])
    return render_template("watched.html", firstname=firstname, lastname=lastname, movies=movies)


@app.route("/search", methods=["POST"])
@login_required
def search():
    firstname = db.execute("SELECT firstname FROM users WHERE id = ?", session["user_id"])[0]["firstname"].title()
    lastname = db.execute("SELECT lastname FROM users WHERE id = ?", session["user_id"])[0]["lastname"].title()

    movie_ids = []
    key = "309f41f5933865be0d2bb63e3bcd2caa"
    name = request.form.get("search")
    results = (requests.get(f"https://api.themoviedb.org/3/search/movie?query={name}&api_key={key}")).json()["results"]
    for result in results:
        movie_ids.append(result["id"])
    return render_template("search.html", firstname=firstname, lastname=lastname, ids=movie_ids)

