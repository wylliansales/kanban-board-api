from repository import task_repository

def create_task(title, description, column_id, order):
    return task_repository.create_task(title, description, column_id, order)

def update_task(task_id, title, description, column_id, order):
    task_repository.update_task(task_id, title, description, column_id, order)

def delete_task(task_id):
    task_repository.delete_task(task_id)