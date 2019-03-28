from lamby.models.project import Project
from lamby.models.meta import Meta
from flask import Blueprint, jsonify, request

projects_api_blueprint = Blueprint('projects_api', __name__)


@projects_api_blueprint.route('/<int:project_id>')
def clone_project(project_id):
    response = dict()

    # Determine if the project exists in the database
    project = Project.query.get(project_id)

    if project is None:
        response['message'] = 'Project not found'
        return jsonify(response), 404

    # Add the project title
    response['project_name'] = project.title

    # Fetch all CommitIDs related to the project
    response['commits'] = dict([(commit.id, commit.to_dict())
                                for commit in project.commits])

    # Fetch the head commits
    response['heads'] = dict([(commit.id, commit.to_dict()) for commit in
                              Meta.get_head_commits(project.id)])

    # Fetch the latest commits
    response['latest_commits'] = dict([(commit.id, commit.to_dict()) for commit
                                       in Meta.get_latest_commits(project.id)])

    response['message'] = 'Succesfully fetched project data'
    return jsonify(response), 200


@projects_api_blueprint.route('/projects/<int:project_id>', methods=['POST'])
def push(project_id):
    response = dict()

    # Determine if the project exists in the database
    project = Project.query.get(project_id)

    if project is None:
        response['message'] = 'Project not found'
        return jsonify(response), 404

    # Assert that the user has permission to push to this project
    token = request.headers['Authorization']

    is_authenticated = any(member.api_key == token
                           for member in project.members)

    if token is None or not is_authenticated:
        response['message'] = 'You do not have access to this project'
        return jsonify(response), 401

    if not request.is_json:
        response['message'] = 'Please send a JSON request'
        return jsonify(response), 400
