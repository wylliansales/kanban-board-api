from models.task import Task
from config.database import get_db_connection
from datetime import datetime

def create_task(title, description, column_id, order):
    conn = get_db_connection()
    cursor = conn.cursor()
    date = datetime.utcnow().isoformat()
    cursor.execute("INSERT INTO tasks (title, description, column_id, \"order\", date) VALUES (?, ?, ?, ?, ?)",
                   (title, description, column_id, order, date))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return Task(id=task_id, title=title, description=description, column_id=column_id, order=order, date=date)

def update_task(task_id, title, description, column_id, order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = ?, description = ?, column_id = ?, \"order\" = ? WHERE id = ?",
                   (title, description, column_id, order, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            column_id INTEGER,
            "order" INTEGER,
            date TIMESTAMP,
            FOREIGN KEY (column_id) REFERENCES columns (id)
        )
    """)
    conn.commit()
    conn.close()