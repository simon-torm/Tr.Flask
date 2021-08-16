from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/users')
def about_page():
    return render_template('users.html')


@app.route('/users/<name>')
def user_page(name):
    return render_template('profile_page.html', name=name)


@app.route('/urls')
def urlss():
    return str(app.url_map)


if __name__ == '__main__':
    app.run(port=6080, debug=True)