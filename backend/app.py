from flask import Flask, render_template, request, redirect, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "secret123"


# ---------------------------------------------------------
# DATABASE INIT
# ---------------------------------------------------------
def init_db():
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE,
                password TEXT,
                eth_address TEXT
            )
        """)
        conn.commit()
        conn.close()

init_db()


def db(query, params=(), one=False):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return (rows[0] if rows else None) if one else rows



# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------
@app.route("/")
def home():
    return redirect("/login")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        sid = request.form["student_id"]
        pw = request.form["password"]

        user = db("SELECT * FROM users WHERE student_id = ?", (sid,), one=True)

        if not user:
            error = "Student ID not found"
        elif user[2] != pw:
            error = "Incorrect password"
        else:
            session["student_id"] = sid
            session["eth"] = user[3]
            return redirect("/dashboard")

    return render_template("login.html", error=error)


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        sid = request.form["student_id"]
        pw = request.form["password"]
        cpw = request.form["confirm_password"]
        eth = request.form["eth_address"]

        if pw != cpw:
            error = "Passwords do not match"
            return render_template("register.html", error=error)

        try:
            db("INSERT INTO users (student_id, password, eth_address) VALUES (?, ?, ?)",
               (sid, pw, eth))
            return redirect("/login")
        except:
            error = "Student ID already exists"

    return render_template("register.html", error=error)


# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


# VOTE PAGE
@app.route("/vote")
def vote():
    if "student_id" not in session:
        return redirect("/login")

    candidates = [
        {"id": 1, "name": "Candidate One", "position": "Class Rep", "image": "cand1.jpg"},
        {"id": 2, "name": "Candidate Two", "position": "Class Rep", "image": "cand2.jpg"},
        {"id": 3, "name": "Candidate Three", "position": "Class Rep", "image": "cand3.jpg"},
    ]

    return render_template("vote.html", candidates=candidates)


# RESULTS
@app.route("/results")
def results():
    if "student_id" not in session:
        return redirect("/login")
    return render_template("results.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------------------------------------------------
# REGISTER LOCAL API
# ---------------------------------------------------------
from api.local_api import local_api
app.register_blueprint(local_api, url_prefix="/api/local")


# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)


