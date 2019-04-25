import os

import requests


def create_droplet(deployment_name, model_uri, commit_id):
    payload = {
        'name': deployment_name,
        'region':
            'nyc3',
        'size':
            's-1vcpu-1gb',
        'image':
            'docker-18-04',
        'user_data':
        f'''#cloud-config
runcmd:
    - docker pull lambyml/lamby-deploy:latest
    - docker run --name lamby-deploy -p 80:3000 \
-e ONNX_MODEL_URI="{model_uri}" \
-e ONNX_COMMIT_ID="{commit_id}" \
-e NODE_ENV=production \
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
    return requests.delete(
        f'https://api.digitalocean.com/v2/droplets/{droplet_id}',
        headers={
            'Authorization': f'Bearer {os.getenv("DIGITAL_OCEAN_API_KEY")}'
        },
    ).status_code


def ping_deployed_model(url):
    return requests.get(url).status_code == 200
