from flask import Blueprint, jsonify

greet_blueprint = Blueprint('greet', __name__)


@greet_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'}), 200
