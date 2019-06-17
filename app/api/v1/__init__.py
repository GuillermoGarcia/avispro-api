from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api.v1 import usuarios, personajes, habilidades, combates, combatientes, errores, tokens, firebase
