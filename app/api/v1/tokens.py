from flask import jsonify, g
from app import db
from app.api.v1 import bp
from app.api.v1.auth import basic_auth, token_auth

'''
    End point: Obtener token
    @return: Response => token del usuario actual.
'''
@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def obtener_token():
    token = g.usuario_actual.obtener_token()
    db.session.commit()
    return jsonify({'token': token})

'''
    End point: Revocar token
    @return: Response => Code 204 No Content
'''
@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revocar_token():
    g.usuario_actual.revocar_token()
    db.session.commit()
    return '', 204