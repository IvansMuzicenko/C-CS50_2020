import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import string

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    current_cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]["cash"]

    total_cash = current_cash

    rows = db.execute("SELECT * FROM stocks WHERE user = :user AND amount > 0", user=session["user_id"])

    new_rows = []

    for row in rows:
        symbol_data = lookup(row["symbol"])
        row["price"] = usd(symbol_data["price"])
        row["name"] = symbol_data["name"]
        row["total"] = usd(row["amount"] * symbol_data["price"])
        total_cash = total_cash + (row["amount"] * symbol_data["price"])
        new_rows.append(row)

    return render_template("index.html", rows=new_rows, current_cash=usd(current_cash), total_cash=usd(total_cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        elif not request.form.get("shares"):
            return apology("must provide shares count", 403)

        symbol_data = lookup(request.form.get("symbol"))


        if symbol_data == None:
            return apology("symbol not found", 403)

        current_cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]["cash"]


        shares = float(request.form.get("shares"))
        total = symbol_data["price"]*shares
        symbol = request.form.get("symbol").upper()

        if (current_cash - total) < 0:
            return apology("not enough cash", 403)

        current_cash = current_cash - total

        user_stocks = db.execute("SELECT * FROM stocks WHERE user = :user AND symbol = :symbol", user=session["user_id"], symbol=symbol)

        if not user_stocks:
            db.execute("INSERT INTO stocks (user, symbol, amount) VALUES (:user, :symbol, :amount)", user=session["user_id"], symbol=symbol, amount = 0)
            user_stocks = db.execute("SELECT * FROM stocks WHERE user = :user AND symbol = :symbol", user=session["user_id"], symbol=symbol)

        amount = user_stocks[0]["amount"]

        db.execute("UPDATE stocks SET amount = :amount WHERE user = :user AND symbol = :symbol",
        amount = amount + shares,
        user=session["user_id"],
        symbol=symbol)

        db.execute("INSERT INTO transactions (user, status, symbol, name, price, shares, time) VALUES(:user, :status, :symbol, :name, :price, :shares, CURRENT_TIMESTAMP)",
        user=session["user_id"], status = 1, symbol=symbol, name=symbol_data["name"], price=symbol_data["price"], shares=shares)

        db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash= current_cash, user=session["user_id"])

        flash(f"Bought for {usd(total)}!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM transactions WHERE user = :user", user=session["user_id"])

    return render_template("history.html", rows = rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    status = request.args.get("status")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("Logged in!")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", status=status)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        symbol_data = lookup(request.form.get("symbol").upper())

        if symbol_data == None:
            return apology("quote not found", 403)

        return render_template("quoted.html", name = symbol_data["name"], symbol=symbol_data["symbol"], price=usd(symbol_data["price"]))

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 403)

        elif not (request.form.get("password") == request.form.get("confirmation")):
            return apology("passwords don't match", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) >= 1 :
            return apology("username is already taken", 403)

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash) VALUES(:username, :password)", username=username, password=password)

        return redirect("/login?status=registered")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        elif not request.form.get("shares"):
            return apology("must provide shares count", 403)

        symbol_data = lookup(request.form.get("symbol"))

        if symbol_data == None:
            return apology("symbol not found", 403)

        current_cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])[0]["cash"]

        current_shares = db.execute("SELECT amount FROM stocks WHERE user = :user AND symbol = :symbol", user=session["user_id"], symbol=request.form.get("symbol"))[0]["amount"]

        if float(request.form.get("shares")) > current_shares:
            return apology("not enough shares", 403)

        shares = float(request.form.get("shares"))
        total = symbol_data["price"]*shares
        symbol = request.form.get("symbol").upper()


        current_cash = current_cash + total

        user_stocks = db.execute("SELECT * FROM stocks WHERE user = :user AND symbol = :symbol", user=session["user_id"], symbol=symbol)

        if not user_stocks:
            db.execute("INSERT INTO stocks (user, symbol, amount) VALUES (:user, :symbol, :amount)", user=session["user_id"], symbol=symbol, amount = 0)
            user_stocks = db.execute("SELECT * FROM stocks WHERE user = :user AND symbol = :symbol", user=session["user_id"], symbol=symbol)

        amount = user_stocks[0]["amount"]

        db.execute("UPDATE stocks SET amount = :amount WHERE user = :user AND symbol = :symbol",
        amount = amount - shares,
        user=session["user_id"],
        symbol=symbol)

        db.execute("INSERT INTO transactions (user, status, symbol, name, price, shares, time) VALUES(:user, :status, :symbol, :name, :price, :shares, CURRENT_TIMESTAMP)",
        user=session["user_id"],
        status = 0,
        symbol=symbol,
        name=symbol_data["name"],
        price=symbol_data["price"],
        shares=shares)

        db.execute("UPDATE users SET cash = :cash WHERE id = :user", cash= current_cash, user=session["user_id"])

        flash(f"Sold for {usd(total)}!")

        return redirect("/")

    else:
        rows = db.execute("SELECT * FROM stocks WHERE user = :user AND amount > 0", user=session["user_id"])
        return render_template("sell.html", rows=rows)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
