import jwt
from functools import wraps
from flask import request, jsonify, g # Importar 'g'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Verifica o cabeçalho 'x-access-token'
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            # Retorna um dicionário e o status, o Flask-RESTX irá serializar para JSON
            return {'message': 'Token é necessário!'}, 401
        
        try:
            data = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
            g.current_user_id = data['user_id'] # Armazena o user_id em flask.g
        except:
            # Retorna um dicionário e o status, o Flask-RESTX irá serializar para JSON
            return {'message': 'Token é inválido!'}, 401
        
        # Não passa current_user_id como argumento, pois ele será acessado via g.current_user_id
        return f(*args, **kwargs)
    
    return decorated
