from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import books, person, Admin, reviews
from datetime import datetime
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = person.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    timestamp = datetime.now()

    # if this returns a user, then the email already exists in database
    user = person.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = person(email=email, name=name,
                      password=generate_password_hash(password, method='sha256'), timestamp=timestamp)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/admin')
def admin():
    return render_template('admin.html')


@auth.route('/admin', methods=['POST'])
def admin_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    admins = Admin.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not admins or not check_password_hash(admins.password, password):
        flash('Please check your login details and try again.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.admin'))

    # if the above check passes, then we know the user has the right credentials
    login_user(admins, remember=remember)
    return redirect(url_for('main.adminOP'))


@auth.route('/admin-signup')
def adminsignup():
    return render_template('admin-signup.html')


@auth.route('/admin-signup', methods=['POST'])
def adminsignup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    timestamp = datetime.now()

    # if this returns a admin, then the email already exists in database
    admins = Admin.query.filter_by(email=email).first()

    if admins:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.adminsignup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_admin = Admin(email=email, name=name,
                      password=generate_password_hash(password, method='sha256'), timestamp=timestamp)

    # add the new user to the database
    db.session.add(new_admin)
    db.session.commit()

    return redirect(url_for('auth.admin'))


@auth.route('/search', methods=['POST'])
def search():
    isbn = request.form.get("search")

    book = books.query.all()
    return render_template('profile.html', book=book, name=isbn)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/review/<string:id>', methods=['POST'])
def review(id):
    reviewer = request.form.get('reviewer')
    rating = request.form.get('star')
    review = request.form.get('review')
    detail = books.query.all()
    for i in detail:
        if id == i.isbn:
           title = i.title
           author = i.author
           year = i.year

    rev = reviews(reviewer=reviewer, isbn=id, rating=rating, review=review)
    db.session.add(rev)
    db.session.commit()

    return render_template('review.html', reviewer=reviewer, isbn=id, title=title, author=author, year=year, rating=rating, review=review)
