from flask import Flask,render_template,session,url_for,request,redirect
app = Flask(__name__)

app.secret_key = "jana"

@app.route('/home')
def home():
    return render_template('child.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["name"]
        session["uname"] = username
        return redirect(url_for("user"))
    else:
        if "uname" in session:
            return redirect(url_for("user"))
        return render_template('login.html')
'''doubt on 17th & 18th statements. why we do that?'''

''' from session dictionary, the "uname" keyword is accessed and is copied to 'un' variable'''
@app.route('/user')
def user():
    if "uname" in session:
        un = session["uname"]
        return f"<h4>Hello {un}! welcome to our website !</h4>"
    else:
        return redirect(url_for("login"))



'''deleting an session manually'''
'''similar syntax of deleting an element in a dictionary (using pop)'''
@app.route('/logout')
def logout():
    session.pop("uname",None)
    return redirect(url_for("login"))



if __name__== "__main__":
    app.run(debug=True)