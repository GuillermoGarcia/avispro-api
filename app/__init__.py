import firebase_admin
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from firebase_admin import credentials, firestore

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

try:
    firebase = firebase_admin.initialize_app(credentials.Certificate('app/api/v1/firebase-admin-key.json'), None, 'avispro_api')
except:
    firebase = firebase_admin.get_app('avispro_api')

firestore = firestore.client(firebase)


from app import routes, models

from app.api.v1 import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api/v1')

