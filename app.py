
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from LogginForms import LogginForm, NameCookieForm, NewPlanForm, NewPlanElementForm, \
    RegistrationForm, NewNameForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user,login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:Flask111@localhost/flask_db'
app.permanent_session_lifetime = 60
app.debug = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message = "Please log in to access this page"
login_manager.login_message_category = 'warning'

kargs_base_template = dict()


@login_manager.user_loader
def load_user(user_id):
    # print(user_id)
    return db.session.query(User).get(user_id)


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


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LogginForm()
    registration_form = RegistrationForm()

    if form.submit.data and form.validate_on_submit():
        print("Logging in")
        name = form.name.data
        password = form.password.data
        # print('Data input: ')
        # print(name)
        # print(password)
        user = db.session.query(User).filter(User.login == name).first()
        if user and user.check_password(password):
            login_user(user, remember=form.remember_me.data)
            flash("You were successfully logged in", 'success')
            return  redirect('/')
        else:
            flash("Invalid username/password", 'danger')
            return redirect('/login')

    if registration_form.registration_submit.data and registration_form.validate_on_submit():
        print("register")
        login = registration_form.login.data
        name = registration_form.name.data
        password = registration_form.password.data
        repeat_password = registration_form.repeat_password.data

        if db.session.query(User).filter(User.login == login).first():
            flash("This login is already taken", 'danger')
            return redirect('/login')
        elif not password == repeat_password:
            flash("Passwords do not match", 'danger')
            return redirect('/login')
        elif login and name and password:
            new_user = User()
            new_user.login = login
            new_user.name = name
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            print("New user added")
            flash("You have successfully registered", 'success')
            return redirect('/login')

    return render_template('login_page.html',
                           form=form,
                           registration_form=registration_form,
                           **kargs_base_template)


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user_page():
    form = NewNameForm()
    if form.validate_on_submit():
        current_user.name = form.new_name.data
        db.session.commit()
        flash("You have successfully changed your name", 'success')
        return redirect('/user')

    return render_template('user_page.html',
                           user=current_user,
                           form=form,
                           **kargs_base_template)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out', 'success')
    return redirect('/')


@app.route('/cookie', methods=['GET', 'POST'])
def set_cookie_page():
    form = NameCookieForm()
    if form.validate_on_submit():
        name = form.name.data

        res = make_response(redirect('/'))
        res.set_cookie('name', name, max_age=60)
        flash("You were successfully set a cookies", "success")

        return res

    return render_template('cookie.html', form=form, **kargs_base_template)


@app.route('/plans', methods=['GET', 'POST'])
@login_required
def plans_page():
    form = NewPlanForm()
    if form.validate_on_submit():
        plan_name = form.name.data
        new_plan = Plan(title=plan_name)
        new_plan.user_id = current_user.id
        db.session.add(new_plan)
        db.session.commit()
        print("Added new plan")
        flash(f"\"{plan_name}\" added!", 'success')
        return redirect('/plans')

    plans = db.session.query(Plan).filter(Plan.user_id == current_user.id).all()[::-1] # DESC
    return render_template('plans_page.html',
                           form=form,
                           plan_list = plans,
                           **kargs_base_template)


@app.route('/plan/<int:id>', methods=['GET', 'POST'])
@login_required
def plan_page(id):
    if not bool(db.session.query(Plan).get(id)):
        return "This plan does not exist!", 404

    if not db.session.query(Plan).get(id).user_id == current_user.id:
        flash("You do not have access to this plan", 'danger')
        return redirect('/plans')

    form = NewPlanElementForm()
    print(form.errors)
    if form.validate_on_submit():
        print("!!!")
        date = form.date.data
        text = form.text.data
        materials = form.materials.data

        element = ListElement()
        element.plan_id = id
        element.text = text
        if date:
            element.date = date
        if materials:
            element.materials = materials
        print(materials)

        db.session.add(element)
        db.session.commit()

        print("Added new element")
        flash(f"Added new element!", "success")
        return redirect(f"/plan/{id}")


    elements = db.session.query(ListElement).filter(ListElement.plan_id == id).all()

    return render_template('plan_page.html',
                           form=form,
                           element_list = elements,
                           **kargs_base_template)


@app.route('/user/<name>')
@login_required
def user_name_page(name):
    return redirect('/user')


@app.route('/urls')
def urlss():
    return str(app.url_map)



# Table models

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String(80), unique=True, nullable=False)
    name = sa.Column(sa.String(80), nullable=False)
    password_hash = sa.Column(sa.String(102), nullable=False)
    created_on = sa.Column(sa.DateTime(), default=datetime.utcnow)
    admin = sa.Column(sa.Boolean(), default=False)

    plans = db.relationship("Plan", backref="user")

    def __repr__(self):
        return f"({self.id}) {self.login}: {self.name}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Plan(db.Model):
    __tablename__ = "Plans"
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(80), unique=True, nullable=False)
    user_id = sa.Column(sa.Integer, db.ForeignKey('Users.id', ondelete="SET NULL"))
    created_on = sa.Column(sa.DateTime(), default=datetime.utcnow)
    updated_on = sa.Column(sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    elements = db.relationship('ListElement', backref="plan", cascade="all,delete-orphan")

    def __repr__(self):
        return f"({self.id}) {self.title} ({self.user_id}, {self.created_on})"


class ListElement(db.Model):
    __tablename__ = "ListElements"
    id = sa.Column(sa.Integer, primary_key=True)
    plan_id = sa.Column(sa.Integer, sa.ForeignKey('Plans.id'))
    date = sa.Column(sa.DateTime)
    text = sa.Column(sa.Text)
    materials = sa.Column(sa.Text)

    def __repr__(self):
        return f"!!!!{self.text}"



if __name__ == '__main__':
    app.run(port=6080)
    # db.create_all()