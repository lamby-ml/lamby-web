import requests

from flask import Blueprint, jsonify, request


from lamby.models.commit import Commit
from lamby.filestore import fs

deploy_api_blueprint = Blueprint('deploy_api', __name__)


@deploy_api_blueprint.route('/<int:commit_id>', methods=['POST'])
def deploy_model(project_id, filename):
    response = dict()

    commit = Commit.query.get(commit_id)

    if commit is None:
        response['message'] = 'No commit found with that ID'
        return jsonify(response), 400

    object_link = fs.get_link(f'{commit.project_id}/{commit.id}')

    payload = {
        'name': f'lamby-deploy-{commit.project_id}-{commit.id}',
        'region': 'nyc3',
        'size': 's-2vcpu-1gb',
        'image': 'docker-18-04',
        'user_data': \
            f'''
            #cloud-config

            runcmd:
              - docker pull lambyml/lamby-deploy:latest
              - docker run --name lamby-deploy -p 80:3000 \
                    -e ONNX_MODEL_URI={object_link} \
                    lambyml/lamby-deploy:latest
            '''
    }

    try:
        requests.post(
            'https://api.digitalocean.com/v2/droplets',
            headers={
                'Authorization': f'Bearer {os.getenv("DIGITAL_OCEAN_API_KEY")}'
            },
            json=payload
        )
        
        json = r.json()

        return jsonify(json), 200
    except requests.exceptions.ConnectionError:
        response['message'] = 'Could not connect to API service. Aborting operation.'
    except requests.exceptions.Timeout:
        reponse['message'] = 'Connection timed out. Aborting operation.'
    except requests.exceptions.TooManyRedirects:
        response['message'] = 'Too many redirects. Aborting operation.')
    except requests.exceptions.RequestException as e:
        response['message'] = f'Unknown requests error: {e}'
    except Exception as e:
        response['message'] = f'Unknown error: {e}'
    
    return jsonify(response), 400
    
