from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from .models import User, Admin
from . import db
import sqlite3


# import psycopg2


# try:
#     conn = psycopg2.connect(database="books", user="postgres",
#                             password="1998", host="localhost")
#     print("connected")
# except:
#     print("Server Error: unable to connect to the database")
# mycursor = conn.cursor()

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

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
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'), timestamp=timestamp)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/adminOP')
def adminOP():
    con = sqlite3.connect("project/user.sqlite")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from User")
    rows = cur.fetchall()
    return render_template("adminOP.html", rows = rows)



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


# @auth.route('/signup')
# def signup():
#     return render_template('signup.html')


# @auth.route('/signup', methods=['POST'])
# def signup_post():
#     email = request.form.get('email')
#     name = request.form.get('name')
#     password = request.form.get('password')
#     timestamp = datetime.now()

#     # if this returns a user, then the email already exists in database
#     user = User.query.filter_by(email=email).first()

#     if user:  # if a user is found, we want to redirect back to signup page so user can try again
#         flash('Email address already exists')
#         return redirect(url_for('auth.signup'))

#     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#     new_user = User(email=email, name=name,
#                     password=generate_password_hash(password, method='sha256'), timestamp=timestamp)

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect(url_for('auth.admin'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
