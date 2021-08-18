from flask import Flask, render_template, redirect, url_for, flash
from LogginForm import LogginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some key'


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/users', methods=['get', 'post'])
def about_page():
    form = LogginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        print('Data input: ')
        print(name)
        print(password)
        flash("You were successfully logged in", "success")
        return redirect('/')

    return render_template('users.html', form=form)


@app.route('/users/<name>')
def user_page(name):
    return render_template('profile_page.html', name=name)


@app.route('/urls')
def urlss():
    return str(app.url_map)


if __name__ == '__main__':
    app.run(port=6080, debug=True)