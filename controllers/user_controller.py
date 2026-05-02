from flask import jsonify, g # Importar 'g'
from flask_restx import Namespace, Resource, fields, reqparse # Importar Namespace, Resource, fields, reqparse
from services.user_service import create_user, update_user, delete_user, authenticate_user
from utils.auth import token_required

user_ns = Namespace('users', description='Operações relacionadas a usuários')

# Modelos para documentação Swagger
user_model = user_ns.model('User', {
    'name': fields.String(required=True, description='Nome do usuário'),
    'email': fields.String(required=True, description='Email do usuário'),
    'password': fields.String(required=True, description='Senha do usuário')
})

login_model = user_ns.model('Login', {
    'email': fields.String(required=True, description='Email do usuário'),
    'password': fields.String(required=True, description='Senha do usuário')
})

auth_token_model = user_ns.model('AuthToken', {
    'token': fields.String(description='Token de autenticação JWT')
})

message_model = user_ns.model('Message', {
    'message': fields.String(description='Mensagem de resposta')
})

error_model = user_ns.model('Error', {
    'error': fields.String(description='Mensagem de erro')
})

# Parser para cabeçalho de autorização
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('Authorization', type=str, location='headers', required=True, help='Bearer Token',
                         default='Bearer <seu_token_jwt>')


@user_ns.route('/')
class UserRegister(Resource):
    @user_ns.doc('register_user')
    @user_ns.expect(user_model, validate=True)
    @user_ns.response(201, 'Usuário registrado com sucesso', message_model)
    @user_ns.response(400, 'Dados inválidos', error_model)
    @user_ns.response(409, 'Email já cadastrado', error_model)
    def post(self):
        '''Cria um novo usuário'''
        data = user_ns.payload
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        user = create_user(name, email, password)
        if not user:
            return {'error': 'Email já cadastrado'}, 409
            
        return {'message': 'Usuário registrado com sucesso'}, 201


@user_ns.route('/login')
class UserLogin(Resource):
    @user_ns.doc('login_user')
    @user_ns.expect(login_model, validate=True)
    @user_ns.response(200, 'Login bem-sucedido', auth_token_model)
    @user_ns.response(401, 'Credenciais inválidas', error_model)
    def post(self):
        '''Autentica um usuário e retorna um token JWT'''
        data = user_ns.payload
        email = data.get('email')
        password = data.get('password')

        token = authenticate_user(email, password)
        if token:
            return {'token': token}, 200
        return {'error': 'Email ou senha inválidos'}, 401


@user_ns.route('/<int:user_id>')
@user_ns.param('user_id', 'O identificador único do usuário')
class User(Resource):
    @user_ns.doc('edit_user')
    @user_ns.expect(auth_parser, user_model, validate=True)
    @user_ns.response(200, 'Usuário atualizado com sucesso', message_model)
    @user_ns.response(400, 'Dados inválidos', error_model)
    @user_ns.response(401, 'Não autorizado', error_model)
    @user_ns.response(403, 'Permissão negada', error_model)
    @token_required
    def put(self, user_id):
        '''Atualiza um usuário existente'''
        current_user_id = g.current_user_id # Acessa o ID do usuário logado via g
        if current_user_id != user_id:
            return {'message': 'Permissão negada'}, 403
        
        data = user_ns.payload
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        if not name or not email or not password:
            return {'error': 'Nome, email e password são obrigatórios'}, 400
        
        update_user(user_id, name, email, password)
        return {'message': 'User atualizado com sucesso'}, 200

    # @user_ns.doc('remove_user')
    # @user_ns.expect(auth_parser)
    # @user_ns.response(200, 'Usuário deletado com sucesso', message_model)
    # @user_ns.response(401, 'Não autorizado', error_model)
    # @user_ns.response(403, 'Permissão negada', error_model)
    # @token_required
    # def delete(self, user_id):
    #     '''Deleta um usuário'''
    #     current_user_id = g.current_user_id # Acessa o ID do usuário logado via g
    #     if current_user_id != user_id:
    #         return {'message': 'Permissão negada'}, 403
    #
    #     delete_user(user_id)
    #     return {'message': 'User deletado com sucesso'}, 200
