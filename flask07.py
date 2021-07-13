from flask import Flask, render_template, url_for, redirect, request, session, flash
from datetime import timedelta
import sqlalchemy
''' tutorial on sql alchemy - saving datas permanently'''
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)
app.secret_key = "jana"

@app.route('/home')
@app.route('/')
def home():
    return render_template('child.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        username = request.form["name"]
        session["uname"] = username
        flash(f"Login successful {username}!")
        return redirect(url_for("user"))
    else:
        if "uname" in session:
            name = session["uname"]
            flash(f"{name}, you have already logged in !!")
            return redirect(url_for("user"))
        return render_template('login.html')

@app.route('/user', methods = ["POST", "GET"])
def user():
    email = None
    if "uname" in session:
        un = session["uname"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
        else:
            if "email" in session:
                email = session["email"]
        return render_template('user.html', user=un, email=email)
    else:
        flash("you are not logged in !!")
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    flash("you have been logged out!", "info")
    session.pop("uname", None)
    session.pop("email", None)
    return redirect(url_for("login"))




if __name__== "__main__":
    app.run(debug=True)