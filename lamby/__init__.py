import os

from pathlib import Path


def create_app():
    from flask import Flask

    app = Flask(__name__)
    app = configure_application(app)
    app = connect_database(app)
    app = initialize_filestore(app)
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
    from lamby.database import db
    from lamby.models.user import User  # NOQA: F401
    from lamby.models.project import Project  # NOQA: F401
    from lamby.models.projects import projects  # NOQA: F401
    from lamby.models.commit import Commit  # NOQA: F401
    from lamby.models.commit_attrs import CommitAttrs  # NOQA: F401
    from lamby.models.meta import ProjectMeta  # NOQA: F401

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


def register_bluprints(app):
    # Import controllers
    from lamby.controllers.home import home_blueprint
    from lamby.controllers.auth import auth_blueprint
    from lamby.controllers.profile import profile_blueprint
    from lamby.controllers.projects import projects_blueprint
    from lamby.controllers.model import model_blueprint

    # Import API endpoints
    from lamby.api.greet import greet_blueprint
    from lamby.api.auth import auth_api_blueprint

    # Register controllers
    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    app.register_blueprint(projects_blueprint, url_prefix='/projects')
    app.register_blueprint(model_blueprint, url_prefix='/models')

    # Register API endpoints (all api routes should be prefixed with /api)
    app.register_blueprint(greet_blueprint, url_prefix='/api')
    app.register_blueprint(auth_api_blueprint, url_prefix='/api/auth')

    return app


def configure_ui(app):
    from flask_login import current_user
    from lamby.util.ui import initialize_navlinks

    initialize_navlinks(app, current_user)

    return app
