#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

celery --app=kanban_boards.celery_app:app worker --loglevel=info