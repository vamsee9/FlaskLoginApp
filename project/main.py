from project.models import person
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)
errors = Blueprint('errors', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', uname=current_user.name)

@main.route('/adminOP')
@login_required
def adminOP():
    return render_template("adminOP.html", users=person.query.all())


@errors.app_errorhandler(401)
def error_401(error):
    return render_template('errors/401.html'), 401

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(405)
def error_405(error):
    return render_template('errors/405.html'), 405


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
