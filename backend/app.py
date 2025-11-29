from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# HOME → LOGIN
@app.route("/")
def home():
    return redirect(url_for('login'))

# REGISTER PAGE
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Later: Save user to DB
        return redirect(url_for('login'))
    return render_template("register.html")

# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for('dashboard'))
    return render_template("login.html")

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# VOTE PAGE
@app.route("/vote")
def vote():
    candidates = [
        {"id": 1, "name": "Candidate One", "position": "Class Representative", "image": "cand1.jpg"},
        {"id": 2, "name": "Candidate Two", "position": "Class Representative", "image": "cand2.jpg"},
        {"id": 3, "name": "Candidate Three", "position": "Class Representative", "image": "cand3.jpg"},
    ]
    return render_template("vote.html", candidates=candidates)

# RESULTS PAGE (UPDATED)
@app.route("/results")
def results():
    candidates = [
        {"name": "Candidate One", "position": "Class Representative", "image": "cand1.jpg", "votes": 12},
        {"name": "Candidate Two", "position": "Class Representative", "image": "cand2.jpg", "votes": 9},
        {"name": "Candidate Three", "position": "Class Representative", "image": "cand3.jpg", "votes": 15},
    ]
    return render_template("results.html", candidates=candidates)

# LOGOUT
@app.route("/logout")
def logout():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)


