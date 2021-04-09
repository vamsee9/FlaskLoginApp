from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#init SQLAlchemy so we can use it later in our model
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'J9xE4EWy89Sd1A45Q05C' # for salting passwords
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dn.sqlite'

    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app