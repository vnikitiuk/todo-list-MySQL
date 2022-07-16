import mysql.connector
from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# TODO: pass via env var
# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
app.secret_key = "My Secret key"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Connect to database
mydb = mysql.connector.connect(
  host="localhost",
  user="todo_list",
  password="0000",
  database="todo_list"
)


def execute_select(sql, params=None):
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql, params)
    myvar = mycursor.fetchall()
    mydb.commit()
    mycursor.close()
    return myvar


def execute_insert(sql, vals):
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute(sql, vals)
    mydb.commit()
    mycursor.close()


@app.route("/")
@login_required
def index():
    todo_items = execute_select("SELECT * FROM todo_items WHERE user_id = %(user_id)s",  { 'user_id': session["user_id"] })
    # user_name = execute_select("SELECT name FROM users WHERE id = %(id)s",  { 'id': session["user_id"] })
    return render_template("index.html", todo_items=todo_items)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        name = request.form.get("username")
        if not name or len(execute_select("SELECT * FROM users WHERE username = %(username)s", { 'username': name })) > 0:
            return apology("must provide username or such username exist", 400)

        # Ensure password has 8 symbols
        password = request.form.get("password")
        if len(password) < 8:
            return apology("Password must be 8 or more symbols", 400)

        # Ensure password was confirmed
        elif password != request.form.get("confirmation"):
            return apology("confimation must match the password", 400)

        # Ensure password include numbers, lowercase and uppercase characters
        no_lower = True
        no_upper = True
        no_digit = True

        for symbol in password:
            if symbol.islower():
                no_lower = False
            elif symbol.isupper():
                no_upper = False
            elif symbol.isdigit():
                no_digit = False

        if no_lower or no_upper or no_digit:
            return apology("Password must include numbers, lowercase and uppercase characters", 400)

        # Remember registrant
        execute_insert("INSERT INTO users (username, hash) VALUES(%s, %s)", (name, generate_password_hash(password)))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = execute_select("SELECT * FROM users WHERE username = %(username)s", { 'username': request.form.get("username") })

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")