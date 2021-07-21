from flask import Flask, render_template, url_for, redirect, request, session, flash

#from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from sensitiveinfo import *
''' tutorial on sql alchemy - adding,deleting and updating users'''


app = Flask(__name__)
#MySql configuration
app.config["MYSQL_HOST"] = mysql_host
app.config["MYSQL_USER"] = mysql_user
app.config["MYSQL_PASSWORD"] =mysql_password
app.config["MYSQL_DB"] = mysql_db
#mysql = MySQL(app)
mysql = MySQL(app)
#mysql.init_app(app)


app.secret_key = "jana"




#db.Model is a inheritance from which the functions (such as columns), keywords are used



#to Display all the user details from the db

@app.route('/view')
def viewdb():
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM users")
    if result>0:
        userdetails = cursor.fetchall()
    return render_template('view.html',values=userdetails)




@app.route('/home')
@app.route('/')
def home():
    return render_template('child.html')





@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["name"]
        usermail = request.form["email"]
        session["user"] = username
        session["mail"] = usermail
       #cursor = mysql.get_db().cursor()
        cursor = mysql.connection.cursor()
       # cursor.execute("SELECT email FROM USERS WHERE email = '{%s}'",usermail)
        cursor.execute("INSERT INTO users (name,email) VALUES (%s,%s)",(username,usermail))
        mysql.connection.commit()
        cursor.close()
        flash(f"Login successful {username}!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            name = session["user"]
            flash(f"{name}, you have already logged in !!")
            return redirect(url_for("user"))
    return render_template('login.html')





@app.route('/user', methods = ["POST", "GET"])
def user():
    name = session["user"]
    flash(f"Hello {name}!")
    return render_template('user.html')





@app.route('/logout')
def logout():
    flash("you have been logged out!", "info")
    '''deleting the sessions that was created at the time of login'''
    session.pop("user", None)
    session.pop("mail", None)
    return redirect(url_for("login"))


@app.route('/delete',methods=["POST","GET"])
def rem_ac():
    if request.method == "POST":
        delusrn = request.form["delname"]
        delusrm = request.form["delmail"]
        #users.query.filter_by(name=delusrn,email=delusrm).delete()
        #db.session.commit()
        username = session.get("uname")
        if username:
            session.pop("uname",None)
            '''if a session is found with this user (logged in after a long time)
            , it should delete them as well to avoid flash mssg bug.'''
        flash("Account deleted successfully !!")
        return redirect(url_for("login"))
    return render_template('delete_ac.html')




if __name__== "__main__":
    #db.create_all()
    app.run(debug = True)