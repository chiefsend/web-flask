from flask import Flask

app = Flask(__name__)
app.config['API_URL'] = 'http://localhost:6969'
app.config['SECRET_KEY'] = '0345896u409568540968630498649058609'

import routes
