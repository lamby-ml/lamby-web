import os

from pathlib import Path


def create_app():
    from flask import Flask

    app = Flask(__name__)
    app = configure_application(app)
    app = connect_database(app)
    app = initialize_filestore(app)
    app = initialize_sessions(app)
    app = register_blueprints(app)
    app = configure_frontend(app)

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
    from lamby.database import db
    from lamby.models.user import User  # NOQA
    from lamby.models.project import Project  # NOQA
    from lamby.models.projects import projects  # NOQA
    from lamby.models.commit import Commit  # NOQA
    from lamby.models.commit_attr import CommitAttr  # NOQA
    from lamby.models.meta import Meta  # NOQA
    from lamby.models.deployment import Deployment  # NOQA

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


def initialize_filestore(app):
    from lamby.filestore import fs

    fs.init_app(app)

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


def register_blueprints(app):
    # Import controllers
    from lamby.controllers.home import home_blueprint
    from lamby.controllers.auth import auth_blueprint
    from lamby.controllers.profile import profile_blueprint
    from lamby.controllers.users import users_blueprint
    from lamby.controllers.projects import projects_blueprint
    from lamby.controllers.models import models_blueprint

    # Import API endpoints
    from lamby.api.auth import auth_api_blueprint
    from lamby.api.projects import projects_api_blueprint

    # Register controllers
    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(projects_blueprint, url_prefix='/projects')
    app.register_blueprint(models_blueprint, url_prefix='/models')

    # Register API endpoints (all api routes should be prefixed with /api)
    app.register_blueprint(auth_api_blueprint, url_prefix='/api/auth')
    app.register_blueprint(projects_api_blueprint, url_prefix='/api/projects')

    return app


def configure_frontend(app):
    from flask import request
    from werkzeug.urls import url_encode

    @app.template_global()
    def modify_query(**new_values):
        args = request.args.copy()

        for key, value in new_values.items():
            args[key] = value

        return '{}?{}'.format(request.path, url_encode(args))

    return app
