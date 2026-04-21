import sqlite3
from datetime import datetime
from db import queries
from config import path_db
import os


def init_db():
    # Создаем папку db, если её нет
    if not os.path.exists('db'):
        os.makedirs('db')
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


def update_task(task_id, new_task=None, completed=None):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    # Обновляем текст, если он передан
    if new_task is not None:
        cursor.execute(queries.update_task_text, (new_task, task_id))

    # Обновляем статус, если он передан
    if completed is not None:
        cursor.execute(queries.update_task_status, (completed, task_id))

    conn.commit()
    conn.close()


def get_tasks(filter_type='all'):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    if filter_type == 'all':
        cursor.execute(queries.select_tasks)
    elif filter_type == 'completed':
        cursor.execute(queries.select_tasks_completed)
    elif filter_type == 'uncompleted':
        cursor.execute(queries.select_tasks_uncompleted)
    else:
        cursor.execute(queries.select_tasks)
    tasks = cursor.fetchall()
    conn.close()
    return tasks 


def delete_task(task_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.delete_task, (task_id,))
    conn.commit()
    conn.close()

def delete_completed():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.delete_completed_tasks)
    conn.commit()
    conn.close()

def delete_completed_tasks():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.delete_completed_tasks) # Выполнение запроса на удаление выполненных
    conn.commit()
    conn.close()