# Pull base image
FROM python:3.9.16-slim-buster
LABEL maintainer="Miguel Osuna <osuna.angulo.miguel@gmail.com>"

# Python won't write .pyc files 
ENV PYTHONDONTWRITEBYTECODE 1
# Python buffered gives familiar output to console
ENV PYTHONUNBUFFERED 1
# Dependencies for building Python packages
ENV BUILD_DEPS="build-essential"
# Dependencies for psycopg2 and translation
ENV APP_DEPS="libpq-dev gettext curl"

RUN apt-get update \
    && apt-get install -y ${BUILD_DEPS} ${APP_DEPS} --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \ 
    && rm -rf /usr/share/doc \ 
    && rm -rf /usr/share/man \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean

# Copy dependencies
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install --upgrade pip
RUN pip install pipenv

# Install dependencies
RUN pipenv install --ignore-pipfile --system \
    && pipenv install --ignore-pipfile --dev --system

# Copy the start bash scripts and change their permissions
COPY ./compose/local/app/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY ./compose/local/app/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r$//g' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./compose/local/app/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r$//g' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh

COPY ./compose/local/app/celery/flower/start.sh /start-flower.sh
RUN sed -i 's/\r$//g' /start-flower.sh
RUN chmod +x /start-flower.sh

# Set work directory
WORKDIR /app 

# COPY project 
COPY . /app/