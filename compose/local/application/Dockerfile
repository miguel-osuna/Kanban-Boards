# Pull base image
FROM python:3.8

# Set environment variables 
# Python don't write byte code: it won't write .pyc files 
ENV PYTHONDONTWRITEBYTECODE 1

# Python buffered gives familiar output to console
ENV PYTHONUNBUFFERED 1

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

# Set work directory
WORKDIR /app 

# COPY project 
COPY . /app/