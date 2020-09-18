import os

from flask import Flask, render_template, request, flash, redirect, session, g
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from forms import UserAddForm, LoginForm,UserEditForm, TrainingsForm
from models import db, connect_db, User, Trainings_users, Trainings

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///capstone'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
# toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                is_trainer=form.trainer.data or User.is_trainer.default.arg)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash('Logout', "success")
    return redirect('/login')


##############################################################################
# General user routes:

@app.route('/users')
def list_users():
    """Page with listing of users.

    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', users=users)


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    trainings = Trainings.query.filter_by(trainer_users_id=g.user.id).all()
    return render_template('users/detail.html', user=user, trainings=trainings)

@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"
            user.about = form.about.data

            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Wrong password, please try again.", 'danger')

    return render_template('users/edit.html', form=form, user_id=user.id)

@app.route('/trainings', methods=["GET", "POST"])
def add_training():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = TrainingsForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        date = form.date.data

        training = Trainings(title=title, description=description, date=date,trainer_users_id=g.user.id)
        db.session.add(training)
        db.session.commit()

        return redirect("/")
    else:
        return render_template("trainings/new_trainings.html", form=form)

@app.route('/mytrainings')
def show_my_trainigs():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    id = g.user.id
    trainings = Trainings.query.filter_by(trainer_users_id=id).all()
    return render_template('trainings/trainigs_list.html', trainings=trainings)




@app.route('/trainings/<training_id>')
def trainings_detail(training_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    training = Trainings.query.get_or_404(training_id)
    return render_template('trainings/detail.html', training=training)


@app.route('/trainings/<training_id>/delete', methods=["POST"])
def delete_training(training_id):
    """Delete training."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    Trainings.query.filter_by(id=training_id).delete()
    db.session.commit()

    return redirect("/mytrainings")

@app.route('/trainings/<training_id>/edit', methods=["GET", "POST"])
def edit_training(training_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    training = Trainings.query.get_or_404(training_id)
    form = TrainingsForm(obj=training)

    if form.validate_on_submit():
        training.title=form.title.data
        training.description=form.description.data
        training.date=form.date.data

        db.session.commit()
        return redirect(f"/mytrainings")

    return render_template('trainings/edit.html', form=form)


@app.route('/trainings/all')
def training_list():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    trainings = Trainings.query.all()
    return render_template('trainings/trainigs_list.html', trainings=trainings)

@app.route('/trainings/book')
def training_list_booked():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(g.user.id)
    return render_template('trainings/booked_trainings.html', user=user)




@app.route('/trainings/<training_id>/book', methods=["POST"])
def book_training(training_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    booked = Trainings_users(users_id=g.user.id,trainings_id=training_id)
    db.session.add(booked)
    db.session.commit()

    return redirect("/trainings/all")

@app.route('/trainings/<training_id>/unbook', methods=["POST"])
def unbook_training(training_id):

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    Trainings_users.query.filter_by(users_id=g.user.id,trainings_id=training_id).delete()
    db.session.commit()

    return redirect("/trainings/all")




##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:
        trainers = (User.query.filter_by(is_trainer=True).limit(21).all())

        return render_template('home.html', trainers=trainers)

    else:
        return render_template('login.html')


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
