import os
from job_boards.app import create_app

app = create_app(configuration=os.getenv("APP_CONFIGURATION", "production"))
