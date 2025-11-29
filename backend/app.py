from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home → Login
@app.route('/')
def home():
    return redirect(url_for('login'))


# -------------------
# LOGIN
# -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # You can add DB check later
        return redirect(url_for('vote'))

    return render_template('login.html')


# -------------------
# REGISTER
# -------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # You will add DB saving later, for now just redirect
        return redirect(url_for('login'))

    return render_template('register.html')


# -------------------
# VOTE PAGE
# -------------------
@app.route('/vote')
def vote():
    # TEMPORARY DUMMY CANDIDATES (works for now)
    candidates = [
        {"id": 1, "name": "Candidate One", "position": "President", "image": "cand1.jpg"},
        {"id": 2, "name": "Candidate Two", "position": "President", "image": "cand2.jpg"},
        {"id": 3, "name": "Candidate Three", "position": "President", "image": "cand3.jpg"}
    ]

    return render_template('vote.html', candidates=candidates)


if __name__ == '__main__':
    app.run(debug=True)
