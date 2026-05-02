from models.column import Column
from models.task import Task
from config.database import get_db_connection

def create_column(name, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO columns (name, user_id) VALUES (?, ?)", (name, user_id))
    conn.commit()
    column_id = cursor.lastrowid
    conn.close()
    return Column(id=column_id, name=name, user_id=user_id)

def update_column(column_id, name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE columns SET name = ? WHERE id = ?", (name, column_id))
    conn.commit()
    conn.close()

def delete_column(column_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM columns WHERE id = ?", (column_id,))
    conn.commit()
    conn.close()

def get_columns_with_tasks_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, user_id FROM columns WHERE user_id = ?", (user_id,))
    columns_data = cursor.fetchall()
    
    columns = []
    for col_data in columns_data:
        column = Column(id=col_data[0], name=col_data[1], user_id=col_data[2])
        
        cursor.execute("SELECT id, title, description, column_id, `order`, date FROM tasks WHERE column_id = ? ORDER BY `order`", (column.id,))
        tasks_data = cursor.fetchall()
        
        tasks = []
        for task_data in tasks_data:
            task = Task(id=task_data[0], title=task_data[1], description=task_data[2], column_id=task_data[3], order=task_data[4], date=task_data[5])
            tasks.append(task.__dict__)
        
        column.tasks = tasks
        columns.append(column.__dict__)
    
    conn.close()
    return columns

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS columns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()