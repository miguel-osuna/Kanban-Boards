#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

celery flower --app=job_boards.celery_app:app \
    --basic_auth="${CELERY_FLOWER_USER}":"${CELERY_FLOWER_PASSWORD}"