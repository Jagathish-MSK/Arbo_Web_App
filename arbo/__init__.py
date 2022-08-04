from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = "IamVamshi24509@@45"

from arbo import routes