from flask import Flask,redirect,url_for
'''tutorial on basic flask operations'''
var = Flask(__name__)


@var.route('/home')
def homepage():
    return "This is the log 1 of :<h3> flask  tutorial </h3>"

@var.route('/<value>')
def display(value):
    return f"hello {value} "

''' 
if someone tries to enter 'admin' page, it should redirect to homepage (for security)
'''
@var.route('/admin')
def admin():
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    var.run();