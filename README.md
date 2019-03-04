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

# Initialize the database
flask db init
flask db migrate
flask db upgrade

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

### Updating the database models

```bash
# After making a change to a model, update the database migrations
flask db migrate

# Make sure the tests still pass
pytest

# Commit the database migrations
flask db upgrade
```

```bash
# If you run into any issues, just nuke your database and start over.
rm -rf lamby/database/migrations lamby/database/dev.db lamby/database/prod.db
```

For more information read the [Flask-Migrate Docs](https://flask-migrate.readthedocs.io/en/latest/).
