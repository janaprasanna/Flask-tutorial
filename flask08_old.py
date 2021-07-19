from flask import Flask, render_template, url_for, redirect, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

''' tutorial on sql alchemy - adding,deleting and updating users'''


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "jana"
db = SQLAlchemy(app)



''' db.Model is a inheritance from which the functions (such as columns), keywords are used'''
class users(db.Model):
    _id = db.Column("Id", db.Integer, primary_key=True)
    name = db.Column("Name", db.String(50))
    email = db.Column("Email", db.String(50))
    '''Note:keywords are case sensitive !!'''

    def __init__(self,name,email):
        self.name = name
        self.email = email



@app.route('/view')
def viewdb():
    return render_template('view.html',values=users.query.all())
'''query.all() grabs all the users info and passes them as objects to the view.html template'''
'''a query to check all the users and their info as a new html page'''






@app.route('/home')
@app.route('/')
def home():
    return render_template('child.html')





@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":

        '''permanent session enabled !'''
        username = request.form["name"]
        '''if a new user is filled in html form is grabbed via request.form query'''
        session["uname"] = username
        '''the newly logged-in  user is added to the session'''
        found_usr = users.query.filter_by(name = username).first()
        '''Adding users to the db'''
        if found_usr:
            '''if the user is already found in the db, we are creating a email session 
            (which would have got updated from user() later) for the user'''
            session["email"] = found_usr.email

        else:
            '''email is set to none (later changed, see user()), at the time of login, as the add email feature is 
            is only avail in user function'''
            usr = users(username, "")
            db.session.add(usr)
            db.session.commit()
        ''' if a user is not found, we are adding the user to the db as a new user'''
        flash(f"Login successful {username}!")
        '''after the user gets logged in to the site, we are redirecting him to the /user page to add his email'''
        return redirect(url_for("user"))
    else:
        if "uname" in session:
            '''if the user is already signed in, we are just flashing a mssg to show that the user is already 
            logged in'''
            name = session["uname"]
            flash(f"{name}, you have already logged in !!")
            return redirect(url_for("user"))
        return render_template('login.html')




@app.route('/user', methods = ["POST", "GET"])
def user():
    email = None
    '''updating the new email if the user is present that was set to None (" ")'''
    if "uname" in session:
        un = session["uname"]
        if request.method == "POST":
            email = request.form["email"]
            '''the new email which is typed in from user.html is collected and updated in the session'''
            flash("Email is saved !")
            session["email"] = email
            found_usr = users.query.filter_by(name = un).first()
            '''after filtering out the desired user with the help of filter_by, we are grabbing the entire user info
            in a var and this var is further put under dot operator to access email and update it'''
            found_usr.email = email
            db.session.commit()
            '''after making a change to the db, it needs to be commited every single time.'''

        else:
            if "email" in session:
                '''if the email is already present, it is passed to user.html for 
                displaying it.'''
                email = session["email"]
        return render_template('user.html', user=un, email=email)
    else:
        ''' if the user is not found for the key "uname", it means 
        there was no login session created for anyone.'''

        flash("you are not logged in !!")
        return redirect(url_for("login"))





@app.route('/logout')
def logout():
    flash("you have been logged out!", "info")
    '''deleting the sessions that was created at the time of login'''
    session.pop("uname", None)
    session.pop("email", None)
    return redirect(url_for("login"))


@app.route('/delete',methods=["POST","GET"])
def rem_ac():
    if request.method == "POST":
        delusrn = request.form["delname"]
        delusrm = request.form["delmail"]
        users.query.filter_by(name=delusrn,email=delusrm).delete()
        db.session.commit()
        username = session.get("uname")
        if username:
            session.pop("uname",None)
            '''if a session is found with this user (logged in after a long time)
            , it should delete them as well to avoid flash mssg bug.'''
        flash("Account deleted successfully !!")
        return redirect(url_for("login"))
    return render_template('delete_ac.html')




if __name__== "__main__":
    db.create_all()
    app.run(debug = True)