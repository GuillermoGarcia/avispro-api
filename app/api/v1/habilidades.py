from flask import jsonify, url_for, request, g, abort
from app import db
from app.models import Combate, Combatiente, HabilidadBase, HabilidadPersonaje, Personaje, Usuario
from app.api.v1 import bp
from app.api.v1.errores import peticion_erronea
from app.api.v1.auth import admin_auth
from app import firestore


'''
    End point: Obtener una habilidad base
    @param: URL => idHabilidad, id de la habilidad base.
    @return: Response => datos de la habilidad base en formato JSON.
'''
@bp.route('/habilidades/<string:idHabilidad>', methods=['GET'])
@admin_auth.login_required
def obtener_habilidad(idHabilidad):
    return jsonify(HabilidadBase.query.get_or_404(idHabilidad).to_dict())


'''
    End point: Obtener todas las habilidades base
    @return: Response => Array con los datos de todas las habilidades base en formato JSON.
'''
@bp.route('/habilidades', methods=['GET'])
@admin_auth.login_required
def obtener_habilidades():
    respuesta = []
    for habilidad in HabilidadBase.query:
        respuesta.append(habilidad.to_dict())
    return jsonify(respuesta)


'''
    End point: Crear una o varias habilidad base
    @return: Response => datos de la/s habilidad/es base creadas en formato JSON.
'''
@bp.route('/habilidades', methods=['POST'])
@admin_auth.login_required
def crear_habilidad():
    datos = request.get_json() or None
    for dato in datos:
        if 'idHabilidad' not in dato or 'nombre' not in dato or 'bonusPrincipal' not in dato \
                or 'bonusSecundario' not in dato or 'combate' not in dato or 'tipo' not in dato:
            return peticion_erronea('Debe incluir los campos idHabilidad, nombre, bonusPrincipal, bonusSecundario, combate y tipo.')
        if HabilidadBase.query.filter_by(idHabilidad=dato['idHabilidad']).first():
            return peticion_erronea('La habilidad ya existe.')
        habilidad = HabilidadBase()
        habilidad.from_dict(dato)
        habilidad.check_boolean()
        db.session.add(habilidad)
        db.session.commit()
    respuesta = jsonify(datos)
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for('api.obtener_habilidades')
    return respuesta


'''
    End point: Actualizar una habilidad base
    @param: URL => idHabilidad, id de la habilidad base.
    @return: Response => datos de la habilidad base actualizada en formato JSON.
'''
@bp.route('/habilidades/<string:idHabilidad>', methods=['PUT'])
@admin_auth.login_required
def actualizar_habilidad(idHabilidad):
    habilidad = HabilidadBase.query.get_or_404(idHabilidad)
    datos = request.get_json() or {}
    if 'idHabilidad' in datos:
        return peticion_erronea('No se puede cambiar el id de la habilidad.')
    habilidad.from_dict(datos)
    db.session.commit()
    return jsonify(habilidad.to_dict())


'''
    End point: Borrar una habilidad base
    @param: URL => idHabilidad, id de la habilidad base.
    @return: Response => mensaje con el exito del borrado o 404 si la habilidad no existe.
'''
@bp.route('/habilidades/<string:idHabilidad>', methods=['DELETE'])
@admin_auth.login_required
def borrar_habilidad(idHabilidad):
    habilidad = HabilidadBase.query.get_or_404(idHabilidad)
    db.session.delete(habilidad)
    db.session.commit()
    return jsonify({'mensaje': 'La habilidad {} ha sido borrada con exito.'.format(habilidad.nombre)})


'''
    End point: Borrar una habilidad base
    @param: URL => idHabilidad, id de la habilidad base.
    @return: Response => mensaje con el exito del borrado o 404 si la habilidad no existe.
'''
@bp.route('/firebase', methods=['HEAD'])
@admin_auth.login_required
def actualizar_desde_firebase():
    usuarios = firestore.collection(u'usuarios').get()
    for usuario in usuarios:
        dct = usuario.to_dict()
        if Usuario.query.filter_by(idUsuario=dct['idUsuario']).count() == 0:
            datos = {
                'idUsuario': dct['idUsuario'],
                'alias': dct['alias'],
                'avatar': dct['avatar'],
                'correo': dct['correo'],
                'contrasena': 'A'
            }
            u = Usuario()
            u.from_dict(datos, nuevo_usuario=True)
            db.session.add(u)
            db.session.commit()
            if len(dct['personajes']) > 0:
                for personaje in dct['personajes']:
                    try:
                        pj_doc = firestore.collection(u'personajes').document(u'{}'.format(personaje)).get()
                    except:
                        print(u'Personaje {} no encontrado'.format(personaje))
                    if pj_doc.exists:
                        p_dct = pj_doc.to_dict()
                        if Personaje.query.filter_by(idPersonaje=p_dct['idPersonaje']).count() == 0:
                            p_datos = {
                                'idPersonaje': p_dct['idPersonaje'],
                                'avatar': p_dct['avatar'],
                                'cultura': p_dct['cultura'],
                                'caracteristicas': p_dct['caracteristicas'],
                                'edad': p_dct['edad'],
                                'nivel': p_dct['nivel'],
                                'nombre': p_dct['nombre'],
                                'procedencia': p_dct['procedencia'],
                                'raza': p_dct['raza']
                            }
                            pj = Personaje()
                            pj.from_dict(p_datos, u.idUsuario)
                            db.session.add(pj)
                            db.session.commit()
                            if len(p_dct['habilidades']) > 0:
                                for habilidad in p_dct['habilidades']:
                                    try:
                                        hab_doc = firestore.collection(u'habilidadPersonaje').document(u'{}'.format(habilidad)).get()
                                    except:
                                        print(u'Habilidad {} no encontrada'.format(habilidad))
                                    if hab_doc.exists:
                                        h_dct = hab_doc.to_dict()
                                        if HabilidadPersonaje.query.filter_by(idHabilidadPersonaje=h_dct['idHabilidadPersonaje']).count() == 0:
                                            h_datos = {
                                                'idHabilidadPersonaje': h_dct['idHabilidadPersonaje'],
                                                'personaje_id': pj.idPersonaje,
                                                'habilidad_id': h_dct['idHabilidad'],
                                                'extra': h_dct['extra'],
                                                'pap': h_dct['pap'],
                                                'habilidadUsada': h_dct['habilidadUsada'],
                                                'valorBase': h_dct['valorBase'],
                                            }
                                            hab = HabilidadPersonaje()
                                            hab.from_dict(h_datos)
                                            db.session.add(hab)
                                            db.session.commit()
                                            hab = None
                            pj = None
            u = None
    combates = firestore.collection(u'combate').get()
    for combate in combates:
        c_dct = combate.to_dict()
        if Combate.query.filter_by(idCombate=c_dct['idCombate']).count() == 0:
            c_datos = {
                'idCombate': c_dct['idCombate'],
                'descripcion': c_dct['descripcion'],
                'master_id': c_dct['idMaster'],
                'nombre': c_dct['nombre'],
                'turno': c_dct['turno'],
                'orden': c_dct['orden']
            }
            c = Combate()
            c.from_dict(c_datos)
            db.session.add(c)
            db.session.commit()
            if len(c_dct['idPjs']) > 0:
                for pjs in c_dct['idPjs']:
                    try:
                        cm_doc = firestore.collection(u'combatiente').document(u'{}'.format(pjs)).get()
                    except:
                        print(u'Combatiente {} no encontrado'.format(pjs))
                    if cm_doc.exists:
                        cm_dct = cm_doc.to_dict()
                        if Combatiente.query.filter_by(idCombatiente=cm_dct['idCombatiente']).count() == 0:
                            cm_datos = {
                                'idCombatiente': cm_dct['idCombatiente'],
                                'avatar': cm_dct['avatar'],
                                'iniciativa': cm_dct['iniciativa'],
                                'nombre': cm_dct['nombre'],
                                'reflejos': cm_dct['reflejos'],
                                'velocidadArma': cm_dct['velocidadArma']
                            }
                            cm = Combatiente()
                            cm.from_dict(cm_datos)
                            db.session.add(cm)
                            c.pjs.append(cm)
                            db.session.commit()
            if len(c_dct['idPnjs']) > 0:
                for pnjs in c_dct['idPnjs']:
                    try:
                        cm_doc = firestore.collection(u'combatiente').document(u'{}'.format(pnjs)).get()
                    except:
                        print(u'Combatiente {} no encontrado'.format(pnjs))
                    if cm_doc.exists:
                        cm_dct = cm_doc.to_dict()
                        if Combatiente.query.filter_by(idCombatiente=cm_dct['idCombatiente']).count() == 0:
                            cm_datos = {
                                'idCombatiente': cm_dct['idCombatiente'],
                                'avatar': cm_dct['avatar'],
                                'iniciativa': cm_dct['iniciativa'],
                                'nombre': cm_dct['nombre'],
                                'reflejos': cm_dct['reflejos'],
                                'velocidadArma': cm_dct['velocidadArma']
                            }
                            cm = Combatiente()
                            cm.from_dict(cm_datos)
                            db.session.add(cm)
                            c.pnjs.append(cm)
                            db.session.commit()
    return u'Operación Terminada'
