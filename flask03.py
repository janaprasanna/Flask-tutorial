from flask import Flask,render_template
'''tutorial on template inheritance'''
var = Flask(__name__)

list=[1,2,3,4,5]
@var.route('/home')
def homepage():
    return render_template('child.html',list=list)



if __name__ == "__main__":
    var.run(debug=True);