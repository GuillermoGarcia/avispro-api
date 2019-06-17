from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import Usuario
from app.api.v1.errores import error_respuesta
from app.api.v1.firebase import Firebase

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
admin_auth = HTTPTokenAuth()

'''
    Verificar correo y contraseña. Login.
    @param: correo, correo del usuario.
    @param: contrasena, contraseña del usuaio.
    @return: Boolean => True si correo existe y la contraseña es correcta, False en caso contrario.
'''
@basic_auth.verify_password
def verificar_contrasena(correo, contrasena):
    usuario = Usuario.query.filter_by(correo=correo).first()
    if usuario is None:
        return False
    g.usuario_actual = usuario
    return usuario.verificar_contrasena(contrasena)

'''
    Respuesta de error si acceso sin estar identificado.
    @return: Response => Error 401 Unauthorized.
'''
@basic_auth.error_handler
def basic_auth_error():
    return error_respuesta(401)

'''
    Verificar token. El token provieve de un end point.
    @param: token, token del usuario o token de Firebase.
    @return: Boolean => True si el token es correcto, False en caso contrario.
'''
@token_auth.verify_token
def verificar_token(token):
    print('Token: {}'.format(token))
    g.usuario_actual = Usuario.verificar_token(token) if token else None
    if g.usuario_actual is None:
        idUsuario = Firebase.firebase_verificar_token(token) if token else None
        g.usuario_actual = Usuario.query.filter_by(idUsuario=idUsuario).first()
        print('idUsuario: {}'.format(g.usuario_actual.idUsuario))
    return g.usuario_actual is not None

'''
    Respuesta de error si acceso sin token valido.
    @return: Response => Error 401 Unauthorized.
'''
@token_auth.error_handler
def token_auth_error():
    return error_respuesta(401, "Token no valido")

'''
    Verificar token de administración. El token proviene de un end point
    @param: token, token de administración.
    @return: Boolean => True si el token es correcto, False en caso contrario.
'''
@admin_auth.verify_token
def verificar_admin_token(token):
    admin_token = "n2E5Er10voOIgZwB4f5dibj8FQC3"
    if (token == admin_token):
        return True
    else:
        return False

'''
    Respuesta de error si acceso sin token de administración valido.
    @return: Response => Error 401 Unauthorized.
'''
@admin_auth.error_handler
def admin_token_auth_error():
    return error_respuesta(401, "Admin Token no valido")