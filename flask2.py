from flask import Flask,redirect,url_for,render_template
'''tutorial on reder template'''
var = Flask(__name__)

list =["jana","prasanna","saran","user01"]
@var.route('/')
def homepage():
    return render_template('index.html',data="dummy text to test place holder.")

@var.route('/users')
def post():
    return render_template('index.html',list=list)

if __name__ == "__main__":
    var.run();