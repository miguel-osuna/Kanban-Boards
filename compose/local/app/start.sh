#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

gunicorn --config python:config.gunicorn wsgi:app