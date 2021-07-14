from flask import Flask, render_template, url_for, redirect, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


''' tutorial on sql alchemy - saving datas permanently'''
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
'''users.sqlite3 - 'users' represent the table name that is created to store information of users.'''
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
'''just to avoid some warnings, we are not tracking all the modifications to the db always hence is false'''
app.permanent_session_lifetime = timedelta(minutes=5)
app.secret_key = "jana"
db = SQLAlchemy(app)
'''database object to write queries'''




class users(db.Model):
    _id = db.column("Id",db.integer,primary_key=True)
    name = db.column("Name",db.string(50))
    email = db.column("Email",db.string(50))

    def __init__(self,name,email):
        self.name = name
        self.email = email










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
    db.create_all()
    app.run(debug=True)