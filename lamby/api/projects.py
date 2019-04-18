from flask import Blueprint, jsonify, request

from lamby.database import db
from lamby.models.commit import Commit
from lamby.models.meta import Meta
from lamby.models.project import Project

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


@projects_api_blueprint.route('/status/<int:project_id>', methods=['POST'])
def push_status(project_id):
    response = dict()

    # Determine if the project exists in the database
    project = Project.query.get(project_id)

    if project is None:
        response['message'] = 'Project not found'
        return jsonify(response), 404

    # Assert that the user has permission to push to this project
    token = request.headers['x-auth']

    if token is None:
        response['message'] = '''No credentials provided. Please set the
            x-auth header to be your API token. If you do not have an
            API token, you can create one with the command `lamby auth` or
            manually generate one on lamby web.'''
        return jsonify(response), 401

    if not any(member.api_key == token for member in project.members):
        response['message'] = 'You do not have access to this project'
        return jsonify(response), 401

    if not request.is_json:
        response['message'] = 'Please send a valid JSON request'
        return jsonify(response), 400

    # Parse the request json into a dictionary
    json = request.get_json()

    # Determine which commits are new and need to be uploaded
    response['commits_to_upload'] = dict()

    # Iterate through each file
    for filename, commits in json['log'].items():
        response['commits_to_upload'][filename] = list()

        # Iterate through the commits for each file
        for commit in commits:
            if Commit.query.get(commit['hash']) is None:
                response['commits_to_upload'][filename].append(commit)

    response['message'] = 'Succesfully fetched commits to upload'
    return jsonify(response), 200


@projects_api_blueprint.route('/push/<int:project_id>', methods=['POST'])
def push(project_id):
    response = dict()

    # Determine if the project exists in the database
    project = Project.query.get(project_id)

    if project is None:
        response['message'] = 'Project not found'
        return jsonify(response), 404

    # Assert that the user has permission to push to this project
    token = request.headers['x-auth']

    if token is None:
        response['message'] = '''No credentials provided. Please set the
            "x-auth" header to be your API token. If you do not have an
            API token, you can create one with the command `lamby auth` or
            manually generate one on lamby web.'''

    if not any(member.api_key == token for member in project.members):
        response['message'] = 'You do not have access to this project'
        return jsonify(response), 401

    if not request.is_json:
        response['message'] = 'Please send a valid JSON request'
        return jsonify(response), 400

    # Parse the request json into a dictionary
    json = request.get_json()

    # Add the new commits to the database
    for filename, commits in json['commits_to_upload'].items():
        for commit in commits:
            try:
                db.session.add(Commit(id=commit['hash'],
                                      project_id=project.id,
                                      filename=filename,
                                      timestamp=commit['timestamp'],
                                      message=commit['message']))
                db.session.commit()
            except Exception as e:
                hash = commit['hash']
                response['message'] = f'Failed to add commit {hash}'
                response['error'] = e.__class__.__name__
                return jsonify(response), 400

    # Update the project meta
    for filename, commit in json['meta']['file_head'].items():
        # Search for an existing meta entry for the given filename
        meta = Meta.query.filter_by(project_id=project_id,
                                    filename=filename).first()

        head = Commit.query.get(commit['hash'])
        latest = Commit.query.filter_by(
            project_id=project.id,
            filename=filename
        ).order_by(Commit.timestamp.desc()).first()

        # Create a new meta entry if this is a new file
        if meta is None:
            meta = Meta(project_id=project_id, filename=filename,
                        head=head.id, latest=latest.id)
            db.session.add(meta)
        else:
            # Update the head commit for the given filename
            meta.head = head.id

            # Update the latest commit for the given filename
            meta.latest = latest.id

        try:
            db.session.commit()
        except Exception as e:
            response['message'] = f'Failed to update meta for {filename}'
            response['error'] = str(e)
            return jsonify(response), 400

    response['message'] = f'Succesfully updated {project.title}'
    return jsonify(response), 200
