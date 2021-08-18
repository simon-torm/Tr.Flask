from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from LogginForms import LogginForm, NameCookie

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some key'
# app.permanent_session_lifetime = 60

kargs_base_template = dict()


@app.before_request
def set_session():
    global kargs_base_template
    kargs_base_template = {
        'cookies': request.cookies,
        'session': session
    }

    if 'counter' in session:
        session['counter'] += 1
    else:
        session['counter'] = 1

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', **kargs_base_template)


@app.route('/users', methods=['get', 'post'])
def users():
    form = LogginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        print('Data input: ')
        print(name)
        print(password)
        flash("You were successfully logged in", "success")
        return redirect('/')

    return render_template('users.html', form=form, **kargs_base_template)


@app.route('/cookie', methods=['get', 'post'])
def set_cookie_page():
    form = NameCookie()
    if form.validate_on_submit():
        name = form.name.data

        res = make_response(redirect('/'))
        res.set_cookie("name", name, max_age=60)
        flash("You were successfully set a cookies")

        return res


    return render_template('cookie.html', form=form, **kargs_base_template)


@app.route('/users/<name>')
def user_page(name):
    return render_template('profile_page.html', name=name, **kargs_base_template)


@app.route('/urls')
def urlss():
    return str(app.url_map)


if __name__ == '__main__':
    app.run(port=6080, debug=True)