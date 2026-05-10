import os
from flask import Flask, jsonify, send_from_directory, request
from datetime import datetime
from flask_restx import Api
from flask_cors import CORS

# Importar os Namespaces dos controladores
from controllers.user_controller import user_ns
from controllers.column_controller import column_ns
from controllers.task_controller import task_ns

from config.database_setup import create_tables

# Configurar o Flask para servir arquivos estáticos da pasta 'static' a partir da raiz
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}}) # Aplicar CORS apenas às rotas da API

create_tables()

# Configurar a instância do Flask-RESTx
api = Api(
    app,
    version='1.0',
    title='Kanban Board API',
    description='Uma API RESTful para gerenciar um Kanban Board.',
    doc='/swagger-ui'
)

# Registrar os Namespaces na instância da API
api.add_namespace(user_ns, path='/api/users')
api.add_namespace(column_ns, path='/api/columns')
api.add_namespace(task_ns, path='/api/tasks')


@app.route('/health')
def health():
    now = datetime.now()
    return jsonify({
        "status": "ok",
        "data": now.strftime("%d/%m/%Y"),
        "hora": now.strftime("%H:%M:%S")
    }), 200

# Manipulador de erro para 404 (Página não encontrada)
@app.errorhandler(404)
def not_found(e):
    # Se a requisição não for para a API, serve o index.html do Angular
    if not request.path.startswith('/api/') and not request.path.startswith('/swagger-ui'):
        return send_from_directory(app.static_folder, 'index.html')
    # Caso contrário, é um 404 real para um endpoint da API, então retorna o erro padrão
    return e


if __name__ == '__main__':
    app.run()
