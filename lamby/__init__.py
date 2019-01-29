import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from pathlib import Path


def create_app():
    app = Flask(__name__)
    app = configure_application(app)
    app = connect_database(app)
    app = register_bluprints(app)
    return app


def configure_application(app):
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

    return app


def connect_database(app):
    from lamby.database import db
    from lamby.models.user import User  # NOQA: F401

    db.init_app(app)
    Migrate(app, db, directory='lamby/database/migrations')

    return app


def register_bluprints(app):
    # Import controllers
    from lamby.controllers.home import home_blueprint

    # Import API endpoints
    from lamby.api.greet import greet_blueprint

    # Register controllers
    app.register_blueprint(home_blueprint)

    # Register API endpoints (all api routes should be prefixed with /api)
    app.register_blueprint(greet_blueprint, url_prefix='/api')

    return app
