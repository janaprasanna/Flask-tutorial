from flask import Flask, render_template, url_for, redirect, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
''' tutorial on sql alchemy - adding,deleting and updating users'''


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes = 5)
app.secret_key = "jana"
db = SQLAlchemy(app)




class users(db.Model):
    _id = db.Column("Id", db.Integer, primary_key=True)
    name = db.Column("Name", db.String(50))
    email = db.Column("Email", db.String(50))

    def __init__(self,name,email):
        self.name = name
        self.email = email



@app.route('/view')
def viewdb():
    return render_template('view.html',values=users.query.all())






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
        found_usr = users.query.filter_by(name = username).first()
        if found_usr:
            session["email"] = found_usr.email

        else:
            usr = users(username, "")
            db.session.add(usr)
            db.session.commit()
        ''' if a user is not found, we are adding it to the db'''
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
            found_usr = users.query.filter_by(name = un).first()
            found_usr.email = email
            db.session.commit()

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
    app.run(debug = True)