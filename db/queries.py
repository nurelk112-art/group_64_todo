
create_tasks = """
    CREATE TABLE IF NOT EXISTS tasks(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         task TEXT NOT NULL,
         created_at TEXT NOT NULL,
         completed INTEGER DEFAULT 0
    )   
"""

# CRUD   CREATE - READ - UPDATE - DELETE

# CREATE
insert_task = "INSERT INTO tasks (task, created_at) VALUES(?,?)" 

# READ
select_tasks = 'SELECT id, task, created_at, completed FROM tasks'
select_tasks_completed = 'SELECT id, task, created_at, completed FROM tasks WHERE completed = 1'
select_tasks_uncompleted = 'SELECT id, task, created_at, completed FROM tasks WHERE completed = 0'

# UPDATE
update_task = 'UPDATE tasks SET task = ? WHERE id = ?' 
update_task_status = 'UPDATE tasks SET completed = ? WHERE id = ?' 

# DELETE
delete_task = 'DELETE FROM tasks WHERE id = ?'
delete_completed_tasks = 'DELETE FROM tasks WHERE completed = 1'
