# Pull base image
FROM python:3.8.7-slim-buster
LABEL maintainer="Miguel Osuna <osuna.angulo.miguel@gmail.com>"

# Set environment variables 
# Python won't write .pyc files 
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
    && rm -rf /usr/share/man

# Install dependencies and remove the requirements folder when done
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt \
    && rm -rf /requirements

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