from flask import jsonify, url_for, request, g, abort
from app import db
from app.models import Usuario, Combate, Combatiente
from app.api.v1 import bp
from app.api.v1.errores import peticion_erronea
from app.api.v1.auth import token_auth
from app.api.v1.firebase import Firebase


'''
    End point: Obtener todos los combates
    @return: Response => Array con los datos de todos los combates en formato JSON.
'''
@bp.route('/combates', methods=['GET'])
@token_auth.login_required
def obtener_combates():
    respuesta = []
    for combate in Combate.query:
        respuesta.append(combate.to_dict())
    return jsonify(respuesta)


'''
    End point: Obtener un combate
    @param: URL => idCombate, id del combate.
    @return: Response => datos del combate en formato JSON.
'''
@bp.route('/combates/<string:idCombate>', methods=['GET'])
@token_auth.login_required
def obtener_combate(idCombate):
    combate = Combate.query.get_or_404(idCombate)
    respuesta = jsonify(combate.to_dict())
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_combate', idCombate=idCombate)
    return respuesta


'''
    End point: Obtener personajes jugadores (pjs) del combate
    @param: URL => idCombate, id del combate.
    @return: Response => Array con los datos de los personajes jugadores del combate en formato JSON.
'''
@bp.route('/combates/<string:idCombate>/pjs', methods=['GET'])
@token_auth.login_required
def obtener_combate_pjs(idCombate):
    combate = Combate.query.get_or_404(idCombate)
    pjs = []
    for idPJ in combate.pjs:
        pjs.append(Combatiente.query.filter_by(idCombate=idPJ).first().to_dict())
    respuesta = jsonify(pjs)
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_combate_pjs', idCombate=idCombate)
    return respuesta


'''
    End point: Obtener personajes no jugadores (pnjs) del combate
    @param: URL => idCombate, id del combate.
    @return: Response => Array con los datos de los personajes no jugadores del combate en formato JSON.
'''
@bp.route('/combates/<string:idCombate>/pnjs', methods=['GET'])
@token_auth.login_required
def obtener_combate_pnjs(idCombate):
    combate = Combate.query.get_or_404(idCombate)
    pnjs = []
    for idPNJ in combate.pnjs:
        pnjs.append(Combatiente.query.filter_by(idCombate=idPNJ).first().to_dict())
    respuesta = jsonify(pjs)
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_combate_pnjs', idCombate=idCombate)
    return respuesta


'''
    End point: Crear un combate
    @param: Body => datos del combate en formato JSON.
    @return: Response => datos del nuevo combate en formato JSON.
'''
@bp.route('/combates', methods=['POST'])
@token_auth.login_required
def crear_combate():
    datos = request.get_json() or None
    if 'nombre' not in datos or 'descripcion' not in datos:
        return peticion_erronea('Debe incluir los campos "nombre" y "descripcion".')
    combate = Combate()
    datos['master_id'] = g.usuario_actual.idUsuario
    datos['idCombate'] = Firebase.firebase_crear_combate(datos, g.usuario_actual.nombre)
    combate.from_dict(datos)
    db.session.add(combate)
    db.session.commit()
    respuesta = jsonify(datos)
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_combate', idCombate=combate.idCombate)
    return respuesta


'''
    End point: Unirse combatiente, como personaje jugador, al combate
    @param: URL => idCombate, id del combate.
    @param: URL => idCombatiente, id del combatiente.
    @return: Response => datos del combate en formato JSON.
'''
@bp.route('/combates/<string:idCombate>/pj/<string:idCombatiente>', methods=['POST'])
@token_auth.login_required
def unirse_combatiente_pj(idCombate, idCombatiente):
    combate = Combate.query.get_or_404(idCombate)
    combatiente = Combatiente.query.get_or_404(idCombatiente)
    combate.pjs.append(combatiente)
    db.session.commit()
    Firebase.firebase_actualizar_combate_pjs(combate.idCombate, combate.pjs)
    respuesta = jsonify(combate.to_dict())
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_combate', idCombate=idCombate)
    return respuesta


'''
    End point: Unirse combatiente, como personaje no jugador, al combate
    @param: URL => idCombate, id del combate.
    @param: URL => idCombatiente, id del combatiente.
    @return: Response => datos del combate en formato JSON.
'''
@bp.route('/combates/<string:idCombate>/pnjs/<string:idCombatiente>', methods=['POST'])
@token_auth.login_required
def unirse_combatiente_pnj(idCombate, idCombatiente):
    combate = Combate.query.get_or_404(idCombate)
    combatiente = Combatiente.query.get_or_404(idCombatiente)
    combate.pnjs.append(combatiente)
    db.session.commit()
    Firebase.firebase_actualizar_combate_pnjs(combate.idCombate, combate.pnjs)
    respuesta = jsonify(combate.to_dict())
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_combate', idCombate=idCombate)
    return respuesta


'''
    End point: Actualizar un combate.
    @param: URL => idCombate, id del combate.
    @return: Response => datos actualizados del combate en formato JSON.
'''
@bp.route('/combates/<string:idCombate>', methods=['PUT'])
@token_auth.login_required
def actualizar_combate(idCombate):
    combate = Combate.query.get_or_404(idCombate)
    datos = request.get_json() or {}
    if 'idCombate' in datos:
        return peticion_erronea('No se puede cambiar el id de la combate.')
    combate.from_dict(datos)
    Firebase.firebase_actualizar_combate(combate, g.usuario_actual.nombre)
    db.session.commit()
    respuesta = jsonify(combate.to_dict())
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_combate', idCombate=idCombate)
    return respuesta