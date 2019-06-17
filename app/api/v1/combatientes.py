from flask import jsonify, url_for, request, g, abort
from app import db
from app.models import Usuario, Combatiente
from app.api.v1 import bp
from app.api.v1.errores import peticion_erronea
from app.api.v1.auth import token_auth
from app.api.v1.firebase import Firebase


'''
    End point: Obtener combatiente
    @param: URL => idCombatiente, id del combatiente.
    @param: URL => idHabilidad, id de la habilidad base a aprender.
    @return: Response => datos de la nueva habilidad del personaje en formato JSON.
'''
@bp.route('/combatientes/<string:idCombatiente>', methods=['GET'])
@token_auth.login_required
def obtener_combatiente(idCombatiente):
    respuesta = jsonify(Combatiente.query.get_or_404(idCombatiente).to_dict())
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_combatiente', idCombatiente=idCombatiente)
    return respuesta


'''
    End point: Crear combatiente
    @param: Body => datos del combatiente en formato JSON.
    @return: Response => datos del nuevo combatiente en formato JSON.
'''
@bp.route('/combatientes', methods=['POST'])
@token_auth.login_required
def crear_combatiente():
    datos = request.get_json() or None
    if 'nombre' not in datos or 'iniciativa' not in datos or 'reflejos' not in datos or 'velocidadArma' not in datos:
            return peticion_erronea('Debe incluir los campos Nombre, Iniciativa, Reflejos y velocidadArma.')
    combatiente = Combatiente()
    datos['idCombatiente'] = Firebase.firebase_crear_combatiente(datos)
    combatiente.from_dict(datos)
    db.session.add(combatiente)
    db.session.commit()
    respuesta = jsonify(datos)
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_combatiente', idCombatiente=combatiente.idCombatiente)
    return respuesta


'''
    End point: Actualizar combatiente
    @param: URL => idCombatiente, id del combatiente.
    @return: Response => datos actualizados del combatiente en formato JSON.
'''
@bp.route('/combatientes/<string:idCombatiente>', methods=['PUT'])
@token_auth.login_required
def actualizar_combatiente(idCombatiente):
    combatiente = Combatiente.query.get_or_404(idCombatiente)
    datos = request.get_json() or {}
    if 'idCombatiente' in datos:
        return peticion_erronea('No se puede cambiar el id del combatiente.')
    combatiente.from_dict(datos)
    Firebase.firebase_actualizar_combatiente(datos)
    db.session.commit()
    respuesta = jsonify(combatiente.to_dict())
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_combatiente', idCombatiente=idCombatiente)
    return respuesta
