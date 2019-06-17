from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

'''
    Crear respuesta con código de estado.
    @param: codigo_estado, código de estado.
    @param: mensaje, mensaje opcional a añadir a la respuesta, por defecto nulo.
    @return: Response => Respuesta con el código de estado y un mensaje si es proprocionado.
'''
def error_respuesta(codigo_estado, mensaje=None):
    payload = {'error': HTTP_STATUS_CODES.get(codigo_estado, 'Error Desconocido.')}
    if mensaje:
        payload['message'] = mensaje
    response = jsonify(payload)
    response.status_code = codigo_estado
    return response

'''
    Respuesta por una petición erronea a un end point.
    @param: mensaje, mensaje a devolver junto al código.
    @return: Respone => Error 400 Bad Request y mensaje.
'''
def peticion_erronea(mensaje):
    return error_respuesta(400, mensaje)