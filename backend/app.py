from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import bcrypt

from utils.db import get_db, get_vote_counts
from utils.security import hash_identity

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        student_id = request.form["student_id"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        eth_address = request.form["eth_address"].strip()

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        db = get_db()

        try:
            db.execute("""
                INSERT INTO users(full_name, student_id, email, password, eth_address)
                VALUES (?, ?, ?, ?, ?)
            """, (full_name, student_id, email, hashed_pw, eth_address))
            db.commit()
        except Exception as e:
            print("Register Error:", e)
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

        if not user:
            return render_template("login.html", error="Invalid ID or password")

        if bcrypt.checkpw(password.encode(), user["password"].encode()):
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

    return render_template("dashboard.html", username=session["name"])


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


# ---------------- CAST VOTE (NO BLOCKCHAIN HERE) ----------------
@app.route("/cast_vote", methods=["POST"])
def cast_vote():
    if "student_id" not in session:
        return jsonify({"status": "error", "message": "Not logged in"})

    data = request.get_json()
    candidate_id = data.get("candidate_id")

    if not candidate_id:
        return jsonify({"status": "error", "message": "No candidate selected"})

    # Hash student ID so votes stay anonymous
    student_id = session["student_id"]
    voter_hash = hash_identity(student_id)

    db = get_db()

    # ---- CHECK IF STUDENT ALREADY VOTED ----
    already = db.execute(
        "SELECT * FROM votes WHERE voter_hash=?",
        (voter_hash,)
    ).fetchone()

    if already:
        return jsonify({"status": "error", "message": "You already voted!"})

    # ---- SAVE VOTE IN LOCAL DB ----
    db.execute(
        "INSERT INTO votes(voter_hash, candidate_id) VALUES (?, ?)",
        (voter_hash, candidate_id)
    )
    db.commit()

    # No blockchain here → Frontend handles MetaMask transaction
    return jsonify({"status": "success"})


# ---------------- RESULTS PAGE (LOCAL DB ONLY) ----------------
@app.route("/results")
def results():
    if "student_id" not in session:
        return redirect(url_for("login"))

    # Blockchain vote fetch
    try:
        votes1 = contract.functions.getVotes(1).call()
        votes2 = contract.functions.getVotes(2).call()
        votes3 = contract.functions.getVotes(3).call()
    except Exception as e:
        print("Blockchain error:", e)
        votes1 = votes2 = votes3 = 0

    candidates = [
        {"id": 1, "name": "Candidate One", "position": "Class Representative", "image": "cand1.jpg",
         "votes": votes1},
        {"id": 2, "name": "Candidate Two", "position": "Class Representative", "image": "cand2.jpg",
         "votes": votes2},
        {"id": 3, "name": "Candidate Three", "position": "Class Representative", "image": "cand3.jpg",
         "votes": votes3},
    ]

    return render_template("results.html", candidates=candidates)



# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(debug=True)
