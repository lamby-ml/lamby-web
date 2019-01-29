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
export FLASK_APP='lamby'
export FLASK_ENV='development'

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

### Running tests

```bash
# Run unit tests
pytest

# Run unit tests on `n` cores (n = 4 here)
pytest -n 4
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

For more information read the [Flask-Migrate Docs](https://flask-migrate.readthedocs.io/en/latest/).
