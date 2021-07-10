from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        return redirect(url_for("user",usr=user))
    else:
        return render_template('login.html')

@app.route('/<usr>')
def user(usr):
    return f"<h4> Hi {usr} ! </h4>"



if __name__=="__main__":
    app.run(debug=True)