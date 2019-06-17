from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api.v1 import usuarios, personajes, habilidades, combates, combatientes, errores, tokens, firebase


import requests
from requests.packages import urllib3
print(urllib3.__version__)