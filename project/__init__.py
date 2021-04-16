from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4igorO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1998@localhost:5432/book'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    admin_manager = LoginManager()
    admin_manager.admin_view = "auth.admin"
    admin_manager.init_app(app)

    from .models import person, Admin

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return person.query.get(int(user_id))
    
    @admin_manager.user_loader
    def load_admin(admin_id):
        return Admin.query.get(int(admin_id))
    
  

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .main import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    return app
