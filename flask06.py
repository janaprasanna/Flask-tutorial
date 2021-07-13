from flask import Flask,render_template,url_for,redirect,request,session,flash
from datetime import timedelta
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
            name=session["uname"]
            flash(f"{name}, you have already logged in !!")
            return redirect(url_for("user"))
        return render_template('login.html')

@app.route('/user')
def user():
    if "uname" in session:
        un = session["uname"]
        return render_template('user.html',user=un)
    else:
        flash("you are not logged in !!")
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    if "uname" in session:
        un = session["uname"]
        flash(f"you have been logged out successfuflly {un}!", "info")
    else:
        flash("No users found! please login first!")
    session.pop("uname", None)
    return redirect(url_for("login"))


'''flash("message to be displayed","category")'''




if __name__== "__main__":
    app.run(debug=True)