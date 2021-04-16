from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from .models import books, person, Admin
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


@auth.route('/adminOP')
def adminOP():
    return render_template("adminOP.html", users=person.query.all())


@auth.route('/admin')
def admin():
    return render_template('admin.html')


@auth.route('/admin', methods=['POST'])
def admin_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    admin = Admin.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not admin or not check_password_hash(admin.password, password):
        flash('Please check your login details and try again.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.admin'))

    # if the above check passes, then we know the user has the right credentials
    login_user(admin, remember=remember)
    return redirect(url_for('auth.adminOP'))


# @auth.route('/admin-signup')
# def signup():
#     return render_template('admin-signup.html')


# @auth.route('/admin-signup', methods=['POST'])
# def adminsignup_post():
#     email = request.form.get('email')
#     name = request.form.get('name')
#     password = request.form.get('password')
#     timestamp = datetime.now()

#     # if this returns a admin, then the email already exists in database
#     admin = Admin.query.filter_by(email=email).first()

#     if admin:  # if a user is found, we want to redirect back to signup page so user can try again
#         flash('Email address already exists')
#         return redirect(url_for('auth.signup'))

#     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#     new_admin = Admin(email=email, name=name,
#                     password=generate_password_hash(password, method='sha256'), timestamp=timestamp)

#     # add the new user to the database
#     db.session.add(new_admin)
#     db.session.commit()

#     return redirect(url_for('auth.admin'))

@auth.route('/search', methods=['POST'])
def search():
    isbn=request.form.get("search") 
   

    book = books.query.all()
    return render_template('profile.html', book=book, name=isbn)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
