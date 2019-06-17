from flask import jsonify, url_for, request, g, abort
from app import db
from app.models import Usuario
from app.api.v1 import bp
from app.api.v1.errores import peticion_erronea
from app.api.v1.auth import token_auth
from app.api.v1.firebase import Firebase



'''
    End point: Obtener usuario
    @param: URL => idUsuario, id del usuario.
    @return: Response => datos del usuario en formato JSON.
'''
@bp.route('/usuarios/<string:idUsuario>', methods=['GET'])
@token_auth.login_required
def obtener_usuario(idUsuario):
    return jsonify(Usuario.query.get_or_404(idUsuario).to_dict())


'''
    End point: Crear usuario.
    @param: Body => datos del usuario a crear en formato JSON.
    @return: Response => datos del usuario creado en formato JSON.
'''
@bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    datos = request.get_json() or {}
    if 'correo' not in datos or 'alias' not in datos or 'contrasena' not in datos:
        return peticion_erronea('Debe incluir los campos correo electrónico, contraseña y alias.')
    if Usuario.query.filter_by(correo=datos['correo']).first():
        return peticion_erronea('Ya hay un usuario con esa dirección correo de correo electrónico, por favor utilice una dirección de correo electrónico diferente.')
    datos['idUsuario'] = Firebase.firebase_crear_usuario(datos)
    usuario = Usuario()
    usuario.from_dict(datos, nuevo_usuario=True)
    db.session.add(usuario)
    db.session.commit()
    respuesta = jsonify(usuario.to_dict())
    respuesta.status_code = 201
    respuesta.headers['Location'] = url_for(
        'api.obtener_usuario', idUsuario=usuario.idUsuario)
    return respuesta

'''
    End point: Actualizar usuario.
    @param: URL => idUsuario, id del usuario.
    @param: Body => datos del usuario a actualizar en formato JSON.
    @return: Response => datos del usuario actualizado en formato JSON.
'''
@bp.route('/usuarios/<string:idUsuario>', methods=['PUT'])
@token_auth.login_required
def actualizar_usuario(idUsuario):
    if g.usuario_actual.idUsuario != idUsuario:
        abort(403)
    usuario = Usuario.query.get_or_404(idUsuario)
    datos = request.get_json() or {}
    if 'idUsuario' in datos:
        return peticion_erronea('No se puede cambiar el id del Usuario.')
    if 'correo' in datos and datos['correo'] != usuario.correo and \
            Usuario.query.filter_by(correo=datos['correo']).first():
        return peticion_erronea('Por favor, use otra dirección de correo electrónico.')
    if 'alias' in datos and datos['alias'] != usuario.alias and \
            Usuario.query.filter_by(alias=datos['alias']).first():
        return peticion_erronea('Por favor, use otro alias.')
    usuario.from_dict(datos, nuevo_usuario=False)
    Firebase.firebase_actualizar_usuario(usuario)
    db.session.commit()
    return jsonify(usuario.to_dict())
