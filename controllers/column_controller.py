from flask import jsonify, g
from flask_restx import Namespace, Resource, fields, reqparse
from services.column_service import create_column, update_column, delete_column, get_columns_with_tasks_by_user
from utils.auth import token_required

column_ns = Namespace('columns', description='Operações relacionadas a colunas')

# Modelos para documentação Swagger
column_input_model = column_ns.model('ColumnInput', {
    'name': fields.String(required=True, description='Nome da coluna')
})

task_output_model = column_ns.model('TaskOutput', {
    'id': fields.Integer(readOnly=True, description='Identificador único da tarefa'),
    'title': fields.String(required=True, description='Título da tarefa'),
    'description': fields.String(description='Descrição detalhada da tarefa'),
    'column_id': fields.Integer(required=True, description='ID da coluna à qual a tarefa pertence'),
    'order': fields.Integer(required=True, description='Ordem da tarefa dentro da coluna'),
    'date': fields.String(description='Data de criação da tarefa (ISO 8601)')
})

column_output_model = column_ns.model('ColumnOutput', {
    'id': fields.Integer(readOnly=True, description='Identificador único da coluna'),
    'name': fields.String(required=True, description='Nome da coluna'),
    'user_id': fields.Integer(required=True, description='ID do usuário proprietário da coluna'),
    'tasks': fields.List(fields.Nested(task_output_model), description='Lista de tarefas na coluna')
})

message_model = column_ns.model('Message', {
    'message': fields.String(description='Mensagem de resposta')
})

error_model = column_ns.model('Error', {
    'error': fields.String(description='Mensagem de erro')
})

# Parser para cabeçalho de autorização
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('Authorization', type=str, location='headers', required=True, help='Bearer Token',
                         default='Bearer <seu_token_jwt>')


@column_ns.route('/')
class ColumnList(Resource):
    @column_ns.doc('add_column')
    @column_ns.expect(auth_parser, column_input_model, validate=True)
    @column_ns.response(201, 'Coluna criada com sucesso', column_output_model)
    @column_ns.response(400, 'Dados inválidos', error_model)
    @column_ns.response(401, 'Não autorizado', error_model)
    @token_required
    def post(self):
        '''Cria uma nova coluna para o usuário logado'''
        current_user_id = g.current_user_id
        data = column_ns.payload
        name = data.get('name')
        if not name:
            return {'error': 'Name é obrigatório'}, 400
        
        column = create_column(name, current_user_id)
        return column_ns.marshal(column.__dict__, column_output_model), 201


@column_ns.route('/<int:column_id>')
@column_ns.param('column_id', 'O identificador único da coluna')
class Column(Resource):
    @column_ns.doc('edit_column')
    @column_ns.expect(auth_parser, column_input_model, validate=True)
    @column_ns.response(200, 'Coluna atualizada com sucesso', message_model)
    @column_ns.response(400, 'Dados inválidos', error_model)
    @column_ns.response(401, 'Não autorizado', error_model)
    @token_required
    def put(self, column_id):
        '''Atualiza uma coluna existente'''
        # current_user_id = g.current_user_id # Não é usado diretamente aqui, mas o token é validado
        data = column_ns.payload
        name = data.get('name')
        if not name:
            return {'error': 'Name é obrigatório'}, 400
        
        update_column(column_id, name)
        return {'message': 'Column atualizada com sucesso'}, 200

    @column_ns.doc('remove_column')
    @column_ns.expect(auth_parser)
    @column_ns.response(200, 'Coluna deletada com sucesso', message_model)
    @column_ns.response(401, 'Não autorizado', error_model)
    @token_required
    def delete(self, column_id):
        '''Deleta uma coluna'''
        # current_user_id = g.current_user_id # Não é usado diretamente aqui, mas o token é validado
        delete_column(column_id)
        return {'message': 'Column deletada com sucesso'}, 200


@column_ns.route('/user')
class UserColumns(Resource):
    @column_ns.doc('get_user_columns')
    @column_ns.expect(auth_parser)
    @column_ns.response(200, 'Lista de colunas do usuário', fields.List(fields.Nested(column_output_model)))
    @column_ns.response(401, 'Não autorizado', error_model)
    @token_required
    def get(self):
        '''Retorna todas as colunas com suas tarefas para o usuário logado'''
        current_user_id = g.current_user_id
        columns = get_columns_with_tasks_by_user(current_user_id)
        # CORREÇÃO AQUI: Passar column_output_model, não fields.List(fields.Nested(...))
        return column_ns.marshal(columns, column_output_model), 200
