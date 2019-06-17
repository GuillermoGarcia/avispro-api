from flask import jsonify, url_for, request, g, abort
from app import db
from app.models import Usuario, HabilidadBase
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
    return jsonify({ 'mensaje': 'La habilidad {} ha sido borrada con exito.'.format(habilidad.nombre)})


'''
    End point: Borrar una habilidad base
    @param: URL => idHabilidad, id de la habilidad base.
    @return: Response => mensaje con el exito del borrado o 404 si la habilidad no existe.
'''
@bp.route('/firebase', methods=['HEAD'])
@admin_auth.login_required
def actualizar_desde_firebase():
    usuarios = firestore.collection(u'usuarios').get()
    response = []
    for usuario in usuarios:
        dct = usuario.to_dict()
        if Usuario.query.filter_by(idUsuario=dct['idUsuario']).count() == 0:
            datos = {
                'idUsuario': dct['idUsuario'],
                'alias': dct['alias'],
                'avatar': dct['avatar'],
                'correo': dct['correo'],
                'contrasena': 'A',
                'personajes': dct['personajes'],
            }
            u = Usuario()
            u.from_dict(datos, nuevo_usuario=True)
            response.append(u.to_dict())
            db.session.add(u)
            db.session.commit()
            u = None
    return respond

