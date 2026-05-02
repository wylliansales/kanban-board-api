from flask import jsonify, g
from flask_restx import Namespace, Resource, fields, reqparse
from services.task_service import create_task, update_task, delete_task
from utils.auth import token_required

task_ns = Namespace('tasks', description='Operações relacionadas a tarefas')

# Modelos para documentação Swagger
task_input_model = task_ns.model('TaskInput', {
    'title': fields.String(required=True, description='Título da tarefa'),
    'description': fields.String(description='Descrição detalhada da tarefa'),
    'column_id': fields.Integer(required=True, description='ID da coluna à qual a tarefa pertence'),
    'order': fields.Integer(required=True, description='Ordem da tarefa dentro da coluna')
})

task_output_model = task_ns.model('TaskOutput', {
    'id': fields.Integer(readOnly=True, description='Identificador único da tarefa'),
    'title': fields.String(required=True, description='Título da tarefa'),
    'description': fields.String(description='Descrição detalhada da tarefa'),
    'column_id': fields.Integer(required=True, description='ID da coluna à qual a tarefa pertence'),
    'order': fields.Integer(required=True, description='Ordem da tarefa dentro da coluna'),
    'date': fields.String(description='Data de criação da tarefa (ISO 8601)')
})

message_model = task_ns.model('Message', {
    'message': fields.String(description='Mensagem de resposta')
})

error_model = task_ns.model('Error', {
    'error': fields.String(description='Mensagem de erro')
})

# Parser para cabeçalho de autorização
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('Authorization', type=str, location='headers', required=True, help='Bearer Token',
                         default='Bearer <seu_token_jwt>')


@task_ns.route('/')
class TaskList(Resource):
    @task_ns.doc('add_task')
    @task_ns.expect(auth_parser, task_input_model, validate=True)
    @task_ns.response(201, 'Tarefa criada com sucesso', task_output_model)
    @task_ns.response(400, 'Dados inválidos', error_model)
    @task_ns.response(401, 'Não autorizado', error_model)
    @token_required
    def post(self):
        '''Cria uma nova tarefa'''
        # current_user_id = g.current_user_id # Não usado diretamente, mas token_required garante autenticação
        data = task_ns.payload
        title = data.get('title')
        description = data.get('description')
        column_id = data.get('column_id')
        order = data.get('order')
        
        if not title or not column_id or order is None:
            return {'error': 'Title, column_id e order são obrigatórios'}, 400
        
        task = create_task(title, description, column_id, order)
        return task_ns.marshal(task.__dict__, task_output_model), 201


@task_ns.route('/<int:task_id>')
@task_ns.param('task_id', 'O identificador único da tarefa')
class Task(Resource):
    @task_ns.doc('edit_task')
    @task_ns.expect(auth_parser, task_input_model, validate=True)
    @task_ns.response(200, 'Tarefa atualizada com sucesso', message_model)
    @task_ns.response(400, 'Dados inválidos', error_model)
    @task_ns.response(401, 'Não autorizado', error_model)
    @token_required
    def put(self, task_id):
        '''Atualiza uma tarefa existente'''
        # current_user_id = g.current_user_id # Não usado diretamente, mas token_required garante autenticação
        data = task_ns.payload
        title = data.get('title')
        description = data.get('description')
        column_id = data.get('column_id')
        order = data.get('order')
        
        if not title or not column_id or order is None:
            return {'error': 'Title, column_id e order são obrigatórios'}, 400
        
        update_task(task_id, title, description, column_id, order)
        return {'message': 'Task atualizada com sucesso'}, 200

    @task_ns.doc('remove_task')
    @task_ns.expect(auth_parser)
    @task_ns.response(200, 'Tarefa deletada com sucesso', message_model)
    @task_ns.response(401, 'Não autorizado', error_model)
    @token_required
    def delete(self, task_id):
        '''Deleta uma tarefa'''
        # current_user_id = g.current_user_id # Não usado diretamente, mas token_required garante autenticação
        delete_task(task_id)
        return {'message': 'Task deletada com sucesso'}, 200
