# Pull base image
FROM python:3.8.7-slim-buster
LABEL maintainer="Miguel Osuna <osuna.angulo.miguel@gmail.com>"

# Set environment variables 
# Python don't write byte code: it won't write .pyc files 
ENV PYTHONDONTWRITEBYTECODE 1

# Python buffered gives familiar output to console
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* \ 
    && rm -rf /usr/share/doc \ 
    && rm -rf /usr/share/man \

    # Install dependencies
    COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

# Copy start bash scripts and change permissions
COPY ./compose/local/application/start /start
RUN sed -i 's/\r$//g' /start 
RUN chmod +x /start 

COPY ./compose/local/application/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/application/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

# Set work directory
WORKDIR /app 

# COPY project 
COPY . /app/