from flask import Flask,render_template,url_for
app=Flask(__name__)


posts  = [
    {
        'author':'jana',
        'title':'Blog post 1',
        'content':'My first blog post',
        'date':'20th june 2021'
    },
    {
        'author': 'prasanna',
        'title': 'Blog post 2',
        'content': 'My second blog post',
        'date': '19th june 2021'
    }

]
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)


@app.route("/about")
def about():
    return render_template('about.html',title='about')


if __name__ == '__main__':
    app.run(debug=True)
