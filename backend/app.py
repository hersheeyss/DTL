from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("register.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TEMPORARY: let user login without validation
        return redirect("/dashboard")
    return render_template("login.html", error=None)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
@app.route("/vote")
def vote():
    return render_template("vote.html")

@app.route("/results")
def results():
    # Placeholder results — replace with actual backend/blockchain values later
    sample_results = {
        "A": 12,
        "B": 9,
        "C": 15
    }
    return render_template("results.html", results=sample_results)

if __name__ == "__main__":
    app.run(debug=True)
