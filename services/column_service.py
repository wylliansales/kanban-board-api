from repository import column_repository

def create_column(name, user_id):
    return column_repository.create_column(name, user_id)

def update_column(column_id, name):
    column_repository.update_column(column_id, name)

def delete_column(column_id):
    column_repository.delete_column(column_id)

def get_columns_with_tasks_by_user(user_id):
    return column_repository.get_columns_with_tasks_by_user(user_id)