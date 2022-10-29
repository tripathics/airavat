from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required, apology
from cs50 import SQL

app = Flask(__name__)
db = SQL("sqlite:///airavat.db")

app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
@login_required
def admin():
    buses = db.execute("SELECT * FROM bus")
    total = len(buses)
    active = db.execute("SELECT COUNT(id) FROM bus WHERE status IS 1")[0]['COUNT(id)']
    inactive = total - active
    return render_template("admin.html", buses=buses, active=active, inactive=inactive, total=total)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if (request.method == "GET"):
        return render_template("login.html")
    else:
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not (rows[0]["password"] == request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/admin")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # get the username and password from the form
        username = request.form.get("username")
        password = request.form.get("password")
        cnf_password = request.form.get("confirmation")

        # check if the user submitted correctly
        if not username: 
            return apology("must provide username")
        elif not password:
            return apology("must provide password")
        elif not password == cnf_password:
            return apology("passwords do not match")

        # register the user by inserting the user details in the database if user is unique
        try:
            db.execute("INSERT INTO users (username, password) VALUES(?, ?)", username, password)
        except ValueError:
            return apology("Username already exists")
        
        # Now that the user has registered, log them in
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session.clear()
        session["user_id"] = rows[0]["id"]

        flash("You are now registered", category="info")
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/tracker_update", methods=["POST"])
def tracker_update():   # handle location and counts here
    return

@app.route("/register_bus", methods=["POST"])
def register_bus():
    bus_name = request.form.get('busname')
    license = request.form.get('license')

    if bus_name:
        db.execute("INSERT INTO bus (name, license_plate) VALUES(?, ?)", bus_name, license)
    else:
        db.execute("INSERT INTO bus (license_plate) VALUES(?)", license)

    return redirect("/admin")

@app.route("/update_bus", methods=["GET", "POST"])
@login_required
def update_bus():
    if (request.method == "GET"):
        id = request.args.get('id')
        bus = db.execute("SELECT * FROM bus WHERE id IS ?", id)[0]
        return render_template("editbus.html", bus=bus)
    else:
        id = request.form.get('id')
        new_status = 1 if request.form.get('status') == 'active' else 0  
        new_name = request.form.get('busname')
        new_license = request.form.get('license')
        print(new_status, new_name, new_license)
        db.execute("""UPDATE bus 
            SET name=?, status=?, license_plate=? 
            WHERE id IS ?""", 
            new_name, new_status, new_license, id
        )

        flash(f"Bus details updated", category="info")
        return redirect("/admin")

@app.route("/remove", methods=["POST"])
def remove_bus():
    id = request.form.get('id')
    name = db.execute("SELECT name FROM bus WHERE id IS ?", id)[0]['name']
    db.execute("DELETE FROM bus WHERE id IS ?", id)
    flash(f"Bus: '{name}', deleted", category="info")
    return redirect("/admin")

app.run()