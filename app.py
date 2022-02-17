import os
import socket

import dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# We will use a factory function to avoid cyclic imports
def create_app():
    app = Flask(__name__)
    # Many parts of flask will require use to use a secret key so we create one
    app.config['SECRET_KEY'] = '123secret'
    # Turn off SqlAlchemy warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Will configure SQLAlchemy to use SQLite and the file db.sqlite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Init the SQLAlchemy object with our app object
    db.init_app(app)

    # Handle flask-login stuff

    # Create a login manager for flask-login
    login_manager = LoginManager()

    # Init the login manager with our app object
    login_manager.init_app(app)

    # Create a user_loader function. Used by flask-login
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        user = User.query.filter_by(id=user_id).first()
        return user

    # Register the open blueprint with the app object
    from blueprints.open import bp_open
    app.register_blueprint(bp_open)

    # Register the user blueprint with the app object
    from blueprints.user import bp_user
    app.register_blueprint(bp_user)

    from blueprints.api import bp_api
    app.register_blueprint(bp_api, url_prefix='/api/v1.0')

    from blueprints.admin import bp_admin
    app.register_blueprint(bp_admin)

    from blueprints.ajax import bp_ajax
    app.register_blueprint(bp_ajax)

    return app


if __name__ == '__main__':
    dotenv.load_dotenv()
    e = os.environ['HEJ']
    app = create_app()

    app.run()
