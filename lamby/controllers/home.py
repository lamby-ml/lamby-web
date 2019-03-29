from flask import Blueprint, render_template

from lamby.models.project import Project

home_blueprint = Blueprint('home', __name__)


@home_blueprint.route('/')
def index():
    projects = Project.query.limit(15).all()
    return render_template('home.jinja', projects=projects, scope="")
