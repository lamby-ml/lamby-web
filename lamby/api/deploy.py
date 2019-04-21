import os

import requests

from flask import Blueprint, jsonify

from lamby.models.commit import Commit
from lamby.filestore import fs

deploy_api_blueprint = Blueprint('deploy_api', __name__)


@deploy_api_blueprint.route('/<int:commit_id>', methods=['POST'])
def deploy_model(commit_id):
    response = dict()

    commit = Commit.query.get(commit_id)

    if commit is None:
        response['message'] = 'No commit found with that ID'
        return jsonify(response), 400

    object_link = fs.get_link(f'{commit.project_id}/{commit.id}')

    try:
        deployment_name = f'lamby-deploy-{commit.project_id}-{commit.id}'

        droplet_ip = create_droplet(deployment_name, object_link)

        response['message'] = f'Your API is up at {droplet_ip}'

        return jsonify(response), 200
    except requests.exceptions.ConnectionError:
        response['message'] = 'Could not connect to API service.'
    except requests.exceptions.Timeout:
        response['message'] = 'Connection timed out. Aborting operation.'
    except requests.exceptions.TooManyRedirects:
        response['message'] = 'Too many redirects. Aborting operation.'
    except requests.exceptions.RequestException as e:
        response['message'] = f'Unknown requests error: {e}'
    except Exception as e:
        response['message'] = f'Unknown error: {e}'

    return jsonify(response), 400


def create_droplet(deployment_name, model_uri):
    payload = {
        'name': deployment_name,
        'region':
            'nyc3',
        'size':
            's-1vcpu-1gb',
        'image':
            'docker-18-04',
        'user_data':
            f'''# cloud-config

            runcmd:
              - docker pull lambyml/lamby-deploy:latest
              - docker run --name lamby-deploy -p 80:3000 \
                    -e ONNX_MODEL_URI={model_uri} \
                    lambyml/lamby-deploy:latest
            '''
    }

    req = requests.post(
        'https://api.digitalocean.com/v2/droplets',
        headers={
            'Authorization': f'Bearer {os.getenv("DIGITAL_OCEAN_API_KEY")}'
        },
        json=payload
    )

    json = req.json()

    droplet_id = json['droplet']['id']

    # Fetch the droplet IP address
    req = requests.get(
        f'https://api.digitalocean.com/v2/droplets/{droplet_id}',
        headers={
            'Authorization': f'Bearer {os.getenv("DIGITAL_OCEAN_API_KEY")}'
        },
    )

    json = req.json()

    droplet_ip = json['droplet']['networks']['v4'][0]['ip_address']

    return droplet_id, droplet_ip


def delete_droplet(droplet_id):
    requests.delete(
        f'https://api.digitalocean.com/v2/droplets/{droplet_id}',
        headers={
            'Authorization': f'Bearer {os.getenv("DIGITAL_OCEAN_API_KEY")}'
        },
    )


def ping_deployed_model(url):
    return requests.get(url).status_code == 200
