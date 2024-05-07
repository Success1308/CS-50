import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request

# Configure application
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"

app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///birthdays.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        if not name or not month or not day:
            flash("Please provide all details.")
            return redirect("/")
        try:
            month = int(month)
            day = int(day)
        except ValueError:
            flash("Please provide valid month and day.")
            return redirect("/")
        if month < 1 or month > 12 or day < 1 or day > 31:
            flash("Please provide valid month (1-12) and day (1-31).")
            return redirect("/")


        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name, month, day)
        flash("Birthday added successfully!")
        return redirect("/")
    else:
        
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)

if __name__ == "__main__":
    app.run(debug=True)
