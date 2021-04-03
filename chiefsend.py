import os

from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)
app.config['API_URL'] = os.getenv("API_URL") or 'http://localhost:6969'
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") or '0345896u409568540968630498649058609'

app.jinja_env.globals['API_URL'] = app.config['API_URL']

import routes
