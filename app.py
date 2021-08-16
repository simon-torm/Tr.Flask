from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'First page'


@app.route('/about')
def aboutPage():
    return 'This is About page'


if __name__ == '__main__':
    app.run(port=6080, debug=True)