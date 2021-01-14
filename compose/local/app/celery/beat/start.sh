#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

celery beat --app=kanban_boards.celery_app:app --loglevel=info --pidfile= --schedule=