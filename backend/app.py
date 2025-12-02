import os
import sqlite3
import hashlib
from flask import Flask, render_template, request, redirect, session, jsonify, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ==========================================================
# FIXED DATABASE PATH (always points to backend/election.db)
# ==========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "election.db")


# ==========================================================
# PASSWORD HASHING (NO INSTALLATION NEEDED)
# ==========================================================
def hash_password(password):
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt + "$" + hashed

def verify_password(stored, provided):
    salt, hashed = stored.split("$")
    check = hashlib.sha256((salt + provided).encode()).hexdigest()
    return hashed == check


# ==========================================================
# SIMPLE DB FUNCTION
# ==========================================================
def db(query, params=(), one=False):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


# ==========================================================
# HOME → LOGIN REDIRECT
# ==========================================================
@app.route("/")
def home():
    return redirect("/login")


# ==========================================================
# LOGIN PAGE
# ==========================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        sid = request.form["student_id"]
        pw = request.form["password"]

        # Fetch user
        user = db("SELECT * FROM users WHERE student_id = ?", (sid,), one=True)

        if not user:
            return render_template("login.html", error="User does not exist.")

        stored_hash = user[2]  # encrypted password from DB

        # CHECK PASSWORD SECURELY
        if not verify_password(stored_hash, pw):
            return render_template("login.html", error="Incorrect password.")

        # Save login session
        session["student_id"] = user[1]
        session["eth_address"] = user[3]

        return redirect("/dashboard")

    return render_template("login.html")


# ==========================================================
# REGISTER PAGE
# ==========================================================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        sid = request.form["student_id"].strip()
        pw = request.form["password"]
        cpw = request.form["confirm_password"]
        eth = request.form["eth_address"]

        # Validation
        if pw != cpw:
            return render_template("register.html", error="Passwords do not match.")

        # Check if user exists
        exists = db("SELECT * FROM users WHERE student_id = ?", (sid,), one=True)
        if exists:
            return render_template("register.html", error="User ID already exists.")

        # HASH PASSWORD BEFORE SAVING
        hashed_pw = hash_password(pw)

        # Add user securely
        db("INSERT INTO users (student_id, password, eth_address) VALUES (?, ?, ?)",
           (sid, hashed_pw, eth))

        return redirect("/login")

    return render_template("register.html")


# ==========================================================
# DASHBOARD PAGE
# ==========================================================
@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect("/login")
    return render_template("dashboard.html")


# ==========================================================
# VOTE PAGE
# ==========================================================
@app.route("/vote")
def vote():
    if "student_id" not in session:
        return redirect("/login")

    candidates = [
        {"id": 1, "name": "Candidate One", "position": "Class Rep", "image": "cand1.jpg"},
        {"id": 2, "name": "Candidate Two", "position": "Class Rep", "image": "cand2.jpg"},
        {"id": 3, "name": "Candidate Three", "position": "Class Rep", "image": "cand3.jpg"}
    ]

    return render_template("vote.html", candidates=candidates)


# ==========================================================
# RESULTS PAGE
# ==========================================================
@app.route("/results")
def results():
    return render_template("results.html")


# ==========================================================
# LOCAL FALLBACK API
# ==========================================================
@app.route("/api/local/results")
def local_results():
    rows = db("SELECT candidate_id, count FROM local_votes")
    result = {str(cid): count for cid, count in rows}
    return jsonify(result)


@app.route("/api/local/vote", methods=["POST"])
def local_vote():
    data = request.get_json()
    cid = data.get("candidateId")

    db("UPDATE local_votes SET count = count + 1 WHERE candidate_id = ?", (cid,))
    return jsonify({"success": True, "txHash": "LOCALCHAIN_TX_" + str(cid)})


# ==========================================================
# LOGOUT
# ==========================================================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ==========================================================
# RUN APP
# ==========================================================
if __name__ == "__main__":
    app.run(debug=True)
