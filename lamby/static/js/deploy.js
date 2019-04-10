/* eslint-env browser */

const DIGITAL_OCEAN_URI = 'https://api.digitalocean.com/v2';

const getDropletIP = async (token, dropletID) => {
  const opt = {
    headers: {
      Authorization: `Bearer ${token}`
    }
  };

  try {
    const data = await fetch(`${DIGITAL_OCEAN_URI}/droplets/${dropletID}`, opt);
    const json = await data.json();

    return await json.droplet.networks.v4[0].ip;
  } catch (error) {
    return error.message;
  }
};

const createDroplet = async (token, pid, cid, link) => {
  const payload = {
    name: `lamby-deploy-${pid}-${cid}`,
    region: 'nyc3',
    size: 's-1vcpu-1gb',
    image: 'docker-18-04',
    user_data: `#cloud-config
    runcmd:
      - docker pull lambyml/lamby-deploy:latest
      - docker run --name lamby-deploy -p 80:3000 -e ONNX_MODEL_URI=${link} lambyml/lamby-deploy:latest
    `
  };

  const opt = {
    headers: {
      'content-type': 'application/json; charset=UTF-8',
      Authorization: `Bearer ${token}`
    },
    body: payload,
    method: 'POST'
  };

  try {
    const data = await fetch(`${DIGITAL_OCEAN_URI}/droplets`, opt);
    const json = await data.json();

    const dropletID = json.droplet.id;
    return await getDropletIP(token, dropletID);
  } catch (error) {
    throw error;
  }
};
