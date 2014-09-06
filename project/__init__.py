from flask import Flask
import os

app = Flask("project")
app.secret_key = os.getenv('SECRET_KEY', 'ayylmao')

import project.routes
