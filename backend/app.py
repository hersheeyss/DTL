from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils.db import get_db
from utils.security import hash_identity
import bcrypt

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.secret_key = "supersecretkey"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        student_id = request.form["student_id"]
        email = request.form["email"]
        password = request.form["password"]
        eth_address = request.form["eth_address"]

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users(full_name, student_id, email, password, eth_address) VALUES(?,?,?,?,?)",
                (full_name, student_id, email, hashed_pw, eth_address)
            )
            db.commit()
        except Exception as e:
            print("Register error:", e)
            return render_template("register.html", err="Student ID already exists")

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_id = request.form["student_id"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE student_id=?",
            (student_id,)
        ).fetchone()

        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            session["student_id"] = user["student_id"]
            session["name"] = user["full_name"]
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid ID or password")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session.get("name", "Student"))


# ---------------- VOTE PAGE ----------------
@app.route("/vote")
def vote():
    if "student_id" not in session:
        return redirect(url_for("login"))

    candidates = [
        {"id": 1, "name": "Candidate One", "position": "Class Representative", "image": "cand1.jpg"},
        {"id": 2, "name": "Candidate Two", "position": "Class Representative", "image": "cand2.jpg"},
        {"id": 3, "name": "Candidate Three", "position": "Class Representative", "image": "cand3.jpg"},
    ]

    return render_template("vote.html", candidates=candidates)


# ---------------- CAST VOTE ----------------
@app.route("/cast_vote", methods=["POST"])
def cast_vote():
    if "student_id" not in session:
        return jsonify({"status": "error", "message": "Not logged in"}), 400

    data = request.get_json()
    candidate_id = data.get("candidate_id")

    if not candidate_id:
        return jsonify({"status": "error", "message": "No candidate selected"}), 400

    student_id = session["student_id"]
    voter_hash = hash_identity(student_id)

    db = get_db()

    already = db.execute(
        "SELECT * FROM votes WHERE voter_hash=?",
        (voter_hash,)
    ).fetchone()

    if already:
        return jsonify({"status": "error", "message": "You already voted!"}), 400

    db.execute(
        "INSERT INTO votes(voter_hash, candidate_id) VALUES(?, ?)",
        (voter_hash, candidate_id)
    )
    db.commit()

    return jsonify({"status": "success", "message": "Vote submitted!"})


# ---------------- RESULTS ----------------
@app.route("/results")
def results():
    if "student_id" not in session:
        return redirect(url_for("login"))

    db = get_db()

    rows = db.execute("""
        SELECT candidate_id, COUNT(*) AS votes
        FROM votes
        GROUP BY candidate_id
    """).fetchall()

    counts = {row["candidate_id"]: row["votes"] for row in rows}

    candidates = [
        {"name": "Candidate One", "position": "Class Representative", "image": "cand1.jpg",
         "votes": counts.get(1, 0)},
        {"name": "Candidate Two", "position": "Class Representative", "image": "cand2.jpg",
         "votes": counts.get(2, 0)},
        {"name": "Candidate Three", "position": "Class Representative", "image": "cand3.jpg",
         "votes": counts.get(3, 0)},
    ]

    return render_template("results.html", candidates=candidates)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)



