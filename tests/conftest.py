import datetime
import json

import pytest
import pytz
from unittest.mock import Mock

from config.settings import app_config
from job_boards.app import create_app
