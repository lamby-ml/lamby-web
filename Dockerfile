# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:alpine

LABEL Name=lamby-web Version=0.0.1
EXPOSE 5000

WORKDIR /app
ADD . /app

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install pipenv && \
    pipenv install --ignore-pipfile && \
    apk --purge del .build-deps

ENV FLASK_APP=lamby FLASK_ENV=production

CMD ["pipenv", "run", "flask", "run", "--host", "0.0.0.0"]
