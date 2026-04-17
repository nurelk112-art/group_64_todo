
create_tasks = """
    CREATE TABLE IF NOT EXISTS tasks(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         task TEXT NOT NULL,
         created_at TEXT NOT NULL 
    )   
"""

# CRUD   CREATE - READ - UPDATE - DELETE

# CREATE
insert_task = "INSERT INTO tasks (task, created_at) VALUES(?,?)" 

# READ
select_tasks = 'SELECT id, task, created_at FROM tasks'

# UPDATE
update_task = 'UPDATE tasks SET task = ? WHERE id = ?' 

# DELETE
delete_task = 'DELETE FROM tasks WHERE id = ?'
