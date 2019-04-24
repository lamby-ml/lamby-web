# lamby-web

Web Interface for Lamby. Built with Python and Flask.

## Setup

### Creating the development environment

```bash
# Create the virtualenv
pipenv --python 3.7

# Activate the virtualenv
pipenv shell

# Install all project dependencies
pipenv install --dev

# Configure linter
flake8 --install-hook git
git config --bool flake8.strict true
```

To exit the virtualenv type `ctrl+d` or type `deactivate`

## Development

### Running the application

```bash
# Set configuration variables
export FLASK_APP=lamby
export FLASK_ENV=development

export MINIO_ACCESS_KEY=<minio_access_key>
export MINIO_SECRET_KEY=<minio_secret_key>

# Run the application
flask run
```

```bash
# Quickly run the server in a specific environment
FLASK_ENV=production flask run
```

### Linting the code

```bash
# Lint all the code
flake8 .
```

```bash
# Automatically format your code (fix linting errors)
autopep8 --recursive --in-place .
```

```bash
# Sort file imports
isort -rc --atomic .
```

### Running tests

```bash
# Quickly run tests (temporarily sets FLASK_ENV to testing for the current command)
FLASK_ENV=testing pytest -v

# Run verbose unit tests in testing environment (don't forget to change FLASK_ENV when done)
export FLASK_ENV=testing
pytest -v

# Run unit tests on `n` cores (n = 4 here)
FLASK_ENV=testing pytest -v -n 4
```

## Docker

```bash
# Build the image
docker build -t lamby:<tag> .

# Run the image in a container
docker run --name lamby-web -p 5000:5000 -d \
    -e MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY \
    -e MINIO_SECRET_KEY=$MINIO_SECRET_KEY \
    -e SQLALCHEMY_DATABASE_URI=$SQL_ALCHEMY_DATABASE_URI \
    lambyml/lamby-web:latest
```

```bash
# Use docker-compose
ACCESS_KEY=<access_key> SECRET_KEY=<secret_key> docker-compose up
```
