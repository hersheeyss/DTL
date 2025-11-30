from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from utils.db import get_db, init_db
from utils.security import hash_identity
from utils.blockchain import get_blockchain_votes
import bcrypt

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.secret_key = "supersecretkey123"

# Auto-create DB tables
init_db()

# Simple admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect(url_for("login"))


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student_id = request.form["student_id"].strip()
        password = request.form["password"].strip()
        eth_address = request.form["eth_address"].strip()

        if not student_id or not password or not eth_address:
            return render_template("register.html", error="All fields are required.")

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users(student_id, password, eth_address) VALUES(?,?,?)",
                (student_id, hashed_pw, eth_address)
            )
            db.commit()
        except Exception as e:
            print("Register error:", e)
            return render_template("register.html", error="Student ID already exists")

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        student_id = request.form["student_id"].strip()
        password = request.form["password"].strip()

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE student_id=?",
            (student_id,)
        ).fetchone()

        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            session["student_id"] = user["student_id"]
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid ID or password")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", student_id=session["student_id"])


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


# ---------------- CAST VOTE (DB ONLY) ----------------
@app.route("/cast_vote", methods=["POST"])
def cast_vote():
    if "student_id" not in session:
        return jsonify({"status": "error", "message": "Not logged in"})

    data = request.get_json()
    candidate_id = data.get("candidate_id")

    if not candidate_id:
        return jsonify({"status": "error", "message": "No candidate selected"})

    student_id = session["student_id"]
    voter_hash = hash_identity(student_id)

    db = get_db()

    # Double voting check
    exists = db.execute(
        "SELECT * FROM votes WHERE voter_hash=?",
        (voter_hash,)
    ).fetchone()

    if exists:
        return jsonify({"status": "error", "message": "You have already voted!"})

    db.execute(
        "INSERT INTO votes(voter_hash, candidate_id) VALUES (?, ?)",
        (voter_hash, candidate_id)
    )
    db.commit()

    return jsonify({"status": "success", "message": "Vote recorded"})


# ---------------- RESULTS (DB COUNTS) ----------------
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

    db_counts = {row["candidate_id"]: row["votes"] for row in rows}

    candidates = [
        {
            "id": 1,
            "name": "Candidate One",
            "position": "Class Representative",
            "image": "cand1.jpg",
            "votes": db_counts.get(1, 0)
        },
        {
            "id": 2,
            "name": "Candidate Two",
            "position": "Class Representative",
            "image": "cand2.jpg",
            "votes": db_counts.get(2, 0)
        },
        {
            "id": 3,
            "name": "Candidate Three",
            "position": "Class Representative",
            "image": "cand3.jpg",
            "votes": db_counts.get(3, 0)
        },
    ]

    return render_template("results.html", candidates=candidates)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# =====================================================
#                   ADMIN LOGIN
# =====================================================
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user = request.form["username"].strip()
        pw = request.form["password"].strip()

        if user == ADMIN_USER and pw == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("admin_panel"))

        return render_template("admin_login.html", error="Invalid admin credentials")

    return render_template("admin_login.html")


# ---------------- ADMIN PANEL ----------------
@app.route("/admin")
def admin_panel():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    db = get_db()

    rows = db.execute("""
        SELECT candidate_id, COUNT(*) AS votes
        FROM votes
        GROUP BY candidate_id
    """).fetchall()

    db_counts = {row["candidate_id"]: row["votes"] for row in rows}

    bc_votes = {
        1: get_blockchain_votes(1),
        2: get_blockchain_votes(2),
        3: get_blockchain_votes(3),
    }

    return render_template("admin_panel.html",
                           db_counts=db_counts,
                           bc_votes=bc_votes)


# ---- API: DB results as JSON (for admin.js) ----
@app.route("/admin/db_results")
def admin_db_results():
    if not session.get("admin"):
        return jsonify({"status": "error", "message": "Unauthorized"})

    db = get_db()
    rows = db.execute("""
        SELECT candidate_id, COUNT(*) AS votes
        FROM votes
        GROUP BY candidate_id
    """).fetchall()

    data = {str(row["candidate_id"]): row["votes"] for row in rows}
    return jsonify({"status": "ok", "data": data})


# ---- API: Blockchain results as JSON (for admin.js) ----
@app.route("/admin/blockchain_results")
def admin_blockchain_results():
    if not session.get("admin"):
        return jsonify({"status": "error", "message": "Unauthorized"})

    data = {
        "1": get_blockchain_votes(1),
        "2": get_blockchain_votes(2),
        "3": get_blockchain_votes(3),
    }
    return jsonify({"status": "ok", "data": data})


if __name__ == "__main__":
    app.run(debug=True)


