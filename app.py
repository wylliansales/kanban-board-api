from flask import Flask, jsonify
from datetime import datetime
from flask_restx import Api # Importar Api do flask_restx

# Importar os Namespaces dos controladores (serão definidos em breve)
from controllers.user_controller import user_ns
from controllers.column_controller import column_ns
from controllers.task_controller import task_ns

from config.database_setup import create_tables

app = Flask(__name__)

create_tables()

# Configurar a instância do Flask-RESTx
api = Api(
    app,
    version='1.0',
    title='Kanban Board API',
    description='Uma API RESTful para gerenciar um Kanban Board.',
    doc='/swagger-ui' # Define o endpoint para a documentação Swagger UI
)

# Registrar os Namespaces na instância da API
api.add_namespace(user_ns, path='/api/users')
api.add_namespace(column_ns, path='/api/columns')
api.add_namespace(task_ns, path='/api/tasks')


@app.route('/')
def health():
    now = datetime.now()
    return jsonify({
        "status": "ok",
        "data": now.strftime("%d/%m/%Y"),
        "hora": now.strftime("%H:%M:%S")
    }), 200

if __name__ == '__main__':
    app.run()
