from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from chatbot import ask_question
from auth import (
    create_user,
    authenticate_user
)

app = Flask(__name__)
app.secret_key = "super-secret-key"

@app.route("/")
def landing():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("chat"))

# --------------------------
# Register
# --------------------------

@app.route("/register",methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        success = create_user(username,email,password)
        if success:
            return redirect(url_for("login"))
        error = "User already exists"
    return render_template("register.html",error=error)


# --------------------------
# Login
# --------------------------

@app.route("/login",methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = authenticate_user(email,password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["email"] = user["email"]
            return redirect(url_for("chat"))
        error = "Invalid credentials"
    return render_template("login.html",error=error)


# --------------------------
# Chat
# --------------------------
@app.route("/chat",methods=["GET", "POST"])
def chat():
    if "user_id" not in session:
        return redirect(url_for("login"))
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        answer = ask_question(str(session["user_id"]),question)
    return render_template("index.html",answer=answer,username=session["username"])

# --------------------------
# Logout
# --------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)