import os

from pathlib import Path


def create_app():
    from flask import Flask

    app = Flask(__name__)
    app = configure_application(app)
    app = connect_database(app)
    app = initialize_sessions(app)
    app = register_bluprints(app)
    app = configure_ui(app)

    return app


def configure_application(app):
    from dotenv import load_dotenv

    env = os.getenv('FLASK_ENV')
    dotenv_path = Path('.') / ('%s.env' % env)
    load_dotenv(dotenv_path=dotenv_path)

    if env == 'development':
        app.config.from_object('lamby.config.DevelopmentConfig')
    elif env == 'testing':
        app.config.from_object('lamby.config.TestingConfig')
    elif env == 'production':
        app.config.from_object('lamby.config.ProductionConfig')
    else:
        app.config.from_object('lamby.config.Config')

    # Set application level settings
    app.url_map.strict_slashes = False

    return app


def connect_database(app):
    from flask_migrate import Migrate

    from lamby.database import db
    from lamby.models.user import User  # NOQA: F401

    db.init_app(app)
    Migrate(app, db, directory='lamby/database/migrations')

    return app


def initialize_sessions(app):
    from flask_login import LoginManager

    from lamby.models.user import User

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def register_bluprints(app):
    # Import controllers
    from lamby.controllers.home import home_blueprint
    from lamby.controllers.auth import auth_blueprint
    from lamby.controllers.profile import profile_blueprint

    # Import API endpoints
    from lamby.api.greet import greet_blueprint

    # Register controllers
    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(profile_blueprint, url_prefix='/profile')

    # Register API endpoints (all api routes should be prefixed with /api)
    app.register_blueprint(greet_blueprint, url_prefix='/api')

    return app


def configure_ui(app):
    from flask_login import current_user
    from lamby.util.ui import initialize_navlinks

    initialize_navlinks(app, current_user)

    return app
