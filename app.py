
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from LogginForms import LogginForm, NameCookie, NewPlanForm, NewPlanElement
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as alm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:Flask111@localhost/flask_db'
app.permanent_session_lifetime = 60
app.debug = True

db = SQLAlchemy(app)

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


@app.route('/users', methods=['GET', 'POST'])
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


@app.route('/cookie', methods=['GET', 'POST'])
def set_cookie_page():
    form = NameCookie()
    if form.validate_on_submit():
        name = form.name.data

        res = make_response(redirect('/'))
        res.set_cookie('name', name, max_age=60)
        flash("You were successfully set a cookies")

        return res


    return render_template('cookie.html', form=form, **kargs_base_template)

@app.route('/plans', methods=['GET', 'POST'])
def plans_page():
    form = NewPlanForm()
    if form.validate_on_submit():
        plan_name = form.name.data
        new_plan = Plan(title=plan_name)
        db.session.add(new_plan)
        db.session.commit()
        print("Added new plan")
        flash(f"\"{plan_name}\" added!")
        return redirect('/plans')

    plans = db.session.query(Plan).all()
    return render_template('plans_page.html',
                           form=form,
                           plan_list = plans,
                           **kargs_base_template)


@app.route('/plan/<int:id>', methods=['GET', 'POST'])
def plan_page(id):
    form = NewPlanElement()
    if not bool(db.session.query(Plan).get(id)):
        return "This plan does not exist!", 404

    if form.validate_on_submit():
        date = form.date.data
        text = form.text.data
        materials = form.materials.data

        element = ListElement(plan_id=id, date=date, text=text, materials=materials)
        db.session.add(element)
        db.session.commit()

        print("Added new element")
        flash(f"Added new element!")
        return redirect(f"/plan/{id}")


    elements = db.session.query(ListElement).filter(ListElement.plan_id == id).all()

    return render_template('plan_page.html',
                           form=form,
                           element_list = elements,
                           **kargs_base_template)


@app.route('/users/<name>')
def user_page(name):
    return render_template('profile_page.html', name=name, **kargs_base_template)


@app.route('/urls')
def urlss():
    return str(app.url_map)



# Table models

class User(db.Model):
    __tablename__ = "Users"
    id = alm.Column(alm.Integer, primary_key=True)
    login = alm.Column(alm.String(80), unique=True, nullable=False)
    name = alm.Column(alm.String(80), nullable=False)
    created_on = alm.Column(alm.DateTime(), default=datetime.utcnow)

    plans = db.relationship("Plan", backref="user", cascade="all,delete-orphan")

    def __repr__(self):
        return f"({self.id}) {self.login}: {self.name}"


class Plan(db.Model):
    __tablename__ = "Plans"
    id = alm.Column(alm.Integer, primary_key=True)
    title = alm.Column(alm.String(80), unique=True, nullable=False)
    user_id = alm.Column(alm.Integer, db.ForeignKey('Users.id'))
    created_on = alm.Column(alm.DateTime(), default=datetime.utcnow)
    updated_on = alm.Column(alm.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    elements = db.relationship('ListElement', backref="plan", cascade="all,delete-orphan")

    def __repr__(self):
        return f"({self.id}) {self.title} ({self.user_id}, {self.created_on})"


class ListElement(db.Model):
    __tablename__ = "ListElements"
    id = alm.Column(alm.Integer, primary_key=True)
    plan_id = alm.Column(alm.Integer, alm.ForeignKey('Plans.id'))
    date = alm.Column(alm.DateTime)
    text = alm.Column(alm.Text)
    materials = alm.Column(alm.Text)

    def __repr__(self):
        return f"!!!!{self.text}"





if __name__ == '__main__':
    app.run(port=6080)
    # db.create_all()