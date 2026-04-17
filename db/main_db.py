import sqlite3
from datetime import datetime
from db import queries
from config import path_db


def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.create_tasks)
    conn.commit()
    conn.close()


def add_task(task):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    # Получаем текущую дату и время
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    cursor.execute(queries.insert_task, (task, now))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id, now # Получаем ID и дату


def update_task(task_id, new_task):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.update_task, (new_task, task_id)) 
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.delete_task, (task_id,))
    conn.commit()
    conn.close()