from flask import jsonify, url_for, request, g, abort
from app import db
from app.models import Usuario, Personaje, HabilidadBase, HabilidadPersonaje
from app.api.v1 import bp
from app.api.v1.errores import peticion_erronea
from app.api.v1.auth import token_auth
from app.api.v1.firebase import Firebase


'''
    End point: Obtener personaje
    @param: URL => idPersonaje, id del personaje.
    @return: Response => datos del personaje en formato JSON.
'''
@bp.route('/personajes/<string:idPersonaje>', methods=['GET'])
@token_auth.login_required
def obtener_personaje(idPersonaje):
    return jsonify(Personaje.query.get_or_404(idPersonaje).to_dict())


'''
    End point: Obtener todas las habilidades del personaje
    @param: URL => idPersonaje, id del personaje.
    @return: Response => datos de todas las habilidades del personaje en formato JSON.
'''
@bp.route('/personajes/<string:idPersonaje>/habilidades', methods=['GET'])
@token_auth.login_required
def obtener_habilidades_personaje(idPersonaje):
    habilidades = Personaje.query.get_or_404(idPersonaje).habilidades
    respuesta = []
    for habilidad in habilidades:
        hb = HabilidadBase.query.filter_by(idHabilidad = habilidad.habilidad_id)
        dato = {
            'idHabilidadPersonaje': habilidad.idHabilidadPersonaje,
            'idHabilidad': habilidad.habilidad_id,
            'idPersonaje': habilidad.personaje_id,
            'nombre': hb.nombre,
            'bonusPrincipal': hb.bonusPrincipal,
            'bonusSecundario': hb.bonusSecundario,
            'combate': hb.combate,
            'tipo': hb.tipo,
            'valorBase': habilidad.valorBase,
            'pap': habilidad.pap,
            'extra': habilidad.extra,
            'habilidadUsada': habilidad.habilidadUsada,
        }
        respuesta.append(dato)
    return jsonify(respuesta)


'''
    End point: Obtener una habilidad del personaje
    @param: URL => idPersonaje, id del personaje.
    @param: URL => idHabilidadPersonaje, id de la habilidad del personaje.
    @return: Response => datos de la habilidad del personaje en formato JSON.
'''
@bp.route('/personajes/<string:idPersonaje>/habilidades/<string:idHabilidadPersonaje>', methods=['GET'])
@token_auth.login_required
def obtener_habilidad_personaje(idPersonaje, idHabilidadPersonaje):
    personaje = Personaje.query.get_or_404(idPersonaje)
    habilidad = HabilidadPersonaje.query.get_or_404(idHabilidadPersonaje) or None
    if g.usuario_actual.idUsuario != personaje.usuario_id:
        abort(403)
    if personaje is None:
        return peticion_erronea('El personaje no existe.')
    if habilidad is None:
        return peticion_erronea('El personaje aún no ha aprendido esta habilidad.')
    else:
        respuesta = jsonify(habilidad.to_dict())
        respuesta.status_code = 201
        respuesta.headers['Location'] = url_for('api.obtener_habilidad_personaje',
            idPersonaje=habilidad.personaje_id, idHabilidadPersonaje = habilidad.idHabilidadPersonaje)
        return respuesta


'''
    End point: Obtener todos los personajes del usuario.
    @return: Response => datos de todos los personajes del usuario en formato JSON.
'''
@bp.route('/personajes', methods=['GET'])
@token_auth.login_required
def obtener_personajes():
    personajes = Personaje.query.filter_by(
        usuario_id=g.usuario_actual.idUsuario)
    respuesta = []
    for personaje in personajes:
        respuesta.append(personaje.to_dict())
    return jsonify(respuesta)


'''
    End point: Crear un personaje
    @param: Body => datos del personaje en formato JSON.
    @return: Response => datos del personaje en formato JSON.
'''
@bp.route('/personajes', methods=['POST'])
@token_auth.login_required
def crear_personaje():
    datos = request.get_json() or {}
    if 'nombre' not in datos:
        return peticion_erronea('Debe incluir el campo nombre.')
    if Personaje.query.filter_by(nombre=datos['nombre'], idUsuario=g.usuario_actual.idUsuario).first():
        return peticion_erronea('El usuario ya tiene un personaje con este nombre.')
    datos['idPersonaje'] = Firebase.firebase_crear_personaje(datos)
    personaje = Personaje()
    personaje.from_dict(datos, g.usuario_actual.idUsuario)
    db.session.add(personaje)
    db.session.commit()
    Firebase.firebase_actualizar_usuario_personajes(Usuario.query.get_or_404(g.usuario_actual.idUsuario).personajes)
    respuesta = jsonify(personaje.to_dict())
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_personaje', idPersonaje=personaje.idPersonaje)
    return respuesta


'''
    End point: Aprender una habilidad el personaje
    @param: URL => idPersonaje, id del personaje.
    @param: URL => idHabilidad, id de la habilidad base a aprender.
    @return: Response => datos de la nueva habilidad del personaje en formato JSON.
'''
@bp.route('/personajes/<string:idPersonaje>/habilidades/<string:idHabilidad>', methods=['POST'])
@token_auth.login_required
def aprender_habilidades(idPersonaje, idHabilidad):
    personaje = Personaje.query.get_or_404(idPersonaje)
    if g.usuario_actual.idUsuario != personaje.usuario_id:
        abort(403)
    if personaje is None:
        return peticion_erronea('El personaje no existe.')
    if not HabilidadBase.query.filter_by(idHabilidad=idHabilidad).first():
        return peticion_erronea('La habilidad no existe.')
    datos = request.get_json() or {}
    if 'valorBase' not in datos or 'pap' not in datos or 'extra' not in datos or 'habilidadUsada' not in datos:
        return peticion_erronea('Debe incluir los campos valorBase, pap, extra y habilidadUsada.')
    datos['personaje_id'] = idPersonaje
    datos['habilidad_id'] = idHabilidad
    habilidad = HabilidadPersonaje()
    if habilidad.conocer_habilidad(datos):
        return peticion_erronea('El personaje ya ha aprendido esta habilidad anteriormente.')
    else:
        datos['idHabilidadPersonaje'] = Firebase.firebase_crear_habilidad(datos)
        habilidad.from_dict(datos)
        print(habilidad)
        db.session.add(habilidad)
        db.session.commit()
        respuesta = jsonify(habilidad.to_dict())
        respuesta.status_code = 201
        respuesta.headers['Location'] = url_for('api.obtener_habilidad_personaje',
            idPersonaje=habilidad.personaje_id, idHabilidadPersonaje = habilidad.idHabilidadPersonaje)
        return respuesta


'''
    End point: Actualizar personaje
    @param: URL => idPersonaje, id del personaje.
    @return: Response => datos actualizados del personaje en formato JSON.
'''
@bp.route('/personajes/<string:idPersonaje>', methods=['PUT'])
@token_auth.login_required
def actualizar_personaje(idPersonaje):
    personaje = Personaje.query.get_or_404(idPersonaje)
    if g.usuario_actual.idUsuario != personaje.usuario_id:
        abort(403)
    datos = request.get_json() or {}
    if 'idPersonaje' in datos:
        return peticion_erronea('No se puede cambiar el id del Personaje.')
    personaje.from_dict(datos, personaje.usuario_id)
    Firebase.firebase_actualizar_personaje(personaje)
    db.session.commit()
    return jsonify(personaje.to_dict())


'''
    End point: Actualizar habilidad del personaje
    @param: URL => idPersonaje, id del personaje.
    @param: URL => idHabilidadPersonaje, id de la habilidad del personaje.
    @return: Response => datos de la habilidad actualizada del personaje en formato JSON.
'''
@bp.route('/personajes/<string:idPersonaje>/habilidades/<string:idHabilidadPersonaje>', methods=['PUT'])
@token_auth.login_required
def actualizar_habilidades(idPersonaje, idHabilidadPersonaje):
    personaje = Personaje.query.get_or_404(idPersonaje) or None
    habilidad = HabilidadPersonaje.query.get_or_404(idHabilidadPersonaje) or None
    if g.usuario_actual.idUsuario != personaje.usuario_id:
        abort(403)
    if personaje is None:
        return peticion_erronea('El personaje no existe.')
    datos = request.get_json() or {}
    if not ('valorBase' in datos or 'pap' in datos or 'extra' in datos or 'habilidadUsada' in datos):
        return peticion_erronea('Debe incluir algunos de estos campos: valorBase, pap, extra o habilidadUsada.')
    if habilidad is None:
        return peticion_erronea('El personaje aún no ha aprendido esta habilidad.')
    else:
        habilidad.from_dict(datos)
        Firebase.firebase_actualizar_habilidad(datos)
        respuesta = jsonify(habilidad.to_dict())
        respuesta.status_code = 201
        respuesta.headers['Location'] = url_for('api.obtener_habilidad_personaje',
            idPersonaje=habilidad.personaje_id, idHabilidadPersonaje = habilidad.idHabilidadPersonaje)
        return respuesta

