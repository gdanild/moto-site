from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)
app.config.from_object('config')
db = SQLAlchemy(app)

from web import views
