#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

celery flower --app=job_boards.celery_app:app \
    --broker="${CELERY_BROKER_URL}" \
    --ult-backend="${CELERY_RESULT_BACKEND}" \
    --basic_auth="${CELERY_FLOWER_USER}":"${CELERY_FLOWER_PASSWORD}"