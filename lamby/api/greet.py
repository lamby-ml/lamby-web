from flask import Blueprint, jsonify


greet_blueprint = Blueprint('greet', __name__, url_prefix='/greet')


@greet_blueprint.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'}), 200
