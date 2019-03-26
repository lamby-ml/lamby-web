from flask import Blueprint, jsonify, request

from lamby.models.user import User

auth_api_blueprint = Blueprint('auth_api', __name__)


@auth_api_blueprint.route('/token', methods=['POST'])
def get_api_token():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    response = {}

    if user is None or not user.check_password(data['password']):
        response['message'] = 'Invalid credentials!'
        return jsonify(response), 401

    if user.api_key is None:
        user.generate_new_api_key()

    response['message'] = 'Successfully fetched API key!'
    response['api_key'] = user.api_key

    return jsonify(response), 200
