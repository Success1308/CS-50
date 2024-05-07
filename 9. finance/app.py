# Import necessary modules and libraries
import os
from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Configure the Flask application
app = Flask(__name__)

# Custom Jinja filter for currency formatting
app.jinja_env.filters["usd"] = usd

# Configure session to use the filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Define a function to set cache control headers after each request
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Route for the home page
@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Retrieve owned stocks for the user from the database
    owned = db.execute(
        "SELECT stock,number FROM owned WHERE user_id = ?", session["user_id"]
    )
    total = 0

    # Calculate the total value of the user's portfolio
    for stock in owned:
        stock["price"] = lookup(stock["stock"])["price"]
        stock["value"] = stock["price"] * stock["number"]
        total += stock["value"]
        stock["value"] = usd(stock["price"] * stock["number"])

    # Retrieve the user's available cash balance
    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
    total += cash[0]["cash"]
    total = usd(total)

    # Render the portfolio page with relevant data
    return render_template(
        "index.html", owned=owned, cash=usd(cash[0]["cash"]), total=total
    )


# Route for buying stocks
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # Handle POST request when user submits a buy request
    if request.method == "POST":
        # Check if all required form fields are provided
        if not request.form.get("symbol"):
            return apology("must provide a stock", 400)
        elif not lookup(request.form.get("symbol")):
            return apology("no such stock", 400)
        elif not request.form.get("shares"):
            return apology("How many bro", 400)
        elif not request.form.get("shares").isnumeric():
            return apology("must enter a number", 400)
        elif int(request.form.get("shares")) <= 0:
            return apology("must buy at least one", 400)

        # Retrieve stock and price information
        stock = request.form.get("symbol")
        price = lookup(request.form.get("symbol"))["price"] * int(
            request.form.get("shares")
        )

        # Check if the user has enough funds to make the purchase
        rows = db.execute("SELECT cash from users WHERE id = ?", session["user_id"])
        if price > rows[0]["cash"]:
            return apology("not enough funds", 400)
        else:
            # Update the user's cash balance
            cash = rows[0]["cash"] - price
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"]
            )

            # Update the user's stock portfolio or create a new entry
            data = db.execute(
                "SELECT number FROM owned WHERE user_id = ? AND stock = ?",
                session["user_id"],
                request.form.get("symbol"),
            )
            if data:
                db.execute(
                    "UPDATE owned SET number = ? WHERE user_id = ? AND stock = ?",
                    data[0]["number"] + int(request.form.get("shares")),
                    session["user_id"],
                    request.form.get("symbol"),
                )
            else:
                db.execute(
                    "INSERT INTO owned (user_id,stock,number) VALUES (?,?,?)",
                    session["user_id"],
                    request.form.get("symbol"),
                    int(request.form.get("shares")),
                )

            # Record the transaction in the 'transactions' table
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            db.execute(
                "INSERT INTO transactions (user_id,type,name,price,time,number) VALUES (?,'Bought',?,?,?,?)",
                session["user_id"],
                request.form.get("symbol"),
                lookup(request.form.get("symbol"))["price"],
                date_time,
                int(request.form.get("shares")),
            )

            # Redirect the user to the portfolio page
            return redirect("/")
    else:
        # Render the buy page if it's a GET request
        return render_template("buy.html")


# Route for viewing transaction history
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Retrieve the user's transaction history from the database
    transactions = db.execute(
        "SELECT type, name, price, time, number FROM transactions WHERE user_id = ? ORDER BY time DESC",
        session["user_id"]
    )

    # Render the transaction history page with relevant data
    return render_template("history.html", transactions=transactions)


# Route for user login
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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Route for user logout
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Route for getting a stock quote
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # Handle POST request when user submits a quote request
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide a stock symbol", 400)
        if lookup(request.form.get("symbol")):
            # Retrieve stock information and format the price
            stock = lookup(request.form.get("symbol"))
            stock["price"] = usd(stock["price"])
            return render_template("quoted.html", stock=stock)
        else:
            return apology("No such stock symbol", 400)
    else:
        # Render the quote page if it's a GET request
        return render_template("quote.html")


# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must confirm your password", 400)
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("must check your password again", 400)

        # Check if the username is already in use
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if rows:
            return apology("username already used", 400)

        # Insert the new user into the 'users' table and log them in
        db.execute(
            "INSERT INTO users (username,hash) VALUES (?,?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )
        number = db.execute(
            "SELECT id FROM users WHERE username = ?", request.form.get("username")
        )
        session["user_id"] = number[0]["id"]
        return redirect("/")
    else:
        # Render the registration page if it's a GET request
        return render_template("register.html")


# Route for selling stocks
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    owned = db.execute(
        "SELECT stock,number FROM owned WHERE user_id = ?", session["user_id"]
    )
    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0][
        "cash"
    ]
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must choose a stock", 400)
        elif not request.form.get("shares"):
            return apology("must enter a number", 400)
        elif not request.form.get("shares").isnumeric():
            return apology("must enter a number", 400)
        elif int(request.form.get("shares")) <= 0:
            return apology("must enter a positive number", 400)

        # Loop through the owned stocks to find the selected one
        for stock in owned:
            if stock["stock"] == request.form.get("symbol"):
                if stock["number"] == 0:
                    return apology("you don't have it", 400)
                elif stock["number"] < int(request.form.get("shares")):
                    return apology("you don't have enough", 400)
                elif stock["number"] == int(request.form.get("shares")):
                    # Sell all shares and update cash balance
                    now = datetime.now()
                    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                    db.execute(
                        "DELETE FROM owned WHERE user_id = ? and stock = ?",
                        session["user_id"],
                        stock["stock"],
                    )
                    cash += (
                        int(request.form.get("shares"))
                        * lookup(request.form.get("symbol"))["price"]
                    )
                    db.execute(
                        "UPDATE users SET cash = ? WHERE id = ?",
                        cash,
                        session["user_id"],
                    )
                    db.execute(
                        "INSERT INTO transactions (user_id,type,name,price,time,number) VALUES (?,'Sold',?,?,?,?)",
                        session["user_id"],
                        request.form.get("symbol"),
                        lookup(request.form.get("symbol"))["price"],
                        date_time,
                        int(request.form.get("shares")),
                    )
                else:
                    # Sell some shares and update cash balance
                    now = datetime.now()
                    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                    cash += (
                        int(request.form.get("shares"))
                        * lookup(request.form.get("symbol"))["price"]
                    )
                    db.execute(
                        "UPDATE users SET cash = ? WHERE id = ?",
                        cash,
                        session["user_id"],
                    )
                    db.execute(
                        "INSERT INTO transactions (user_id,type,name,price,time,number) VALUES (?,'Sold',?,?,?,?)",
                        session["user_id"],
                        request.form.get("symbol"),
                        lookup(request.form.get("symbol"))["price"],
                        date_time,
                        int(request.form.get("shares")),
                    )
                    db.execute(
                        "UPDATE owned SET number = ? WHERE user_id = ? and stock = ?",
                        stock["number"] - int(request.form.get("shares")),
                        session["user_id"],
                        stock["stock"],
                    )
        return redirect("/")
    else:
        # Render the sell page if it's a GET request
        return render_template("sell.html", owned=owned)
