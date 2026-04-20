Here's the complete code for `db.py` that handles database operations for a To-Do List application using SQLite with Flask:

```python
import sqlite3
from sqlite3 import Error
from flask import g

DATABASE = 'todo.db'

def get_db():
    """
    Get a database connection from the connection pool.
    If no connection exists, create a new one.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Allows accessing columns by name
    return db

def init_db():
    """
    Initialize the database by creating the tasks table if it doesn't exist.
    """
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed BOOLEAN DEFAULT 0
            )
        ''')
        conn.commit()

def close_db(e=None):
    """
    Close the database connection when the app context ends.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def add_task(title, description=None):
    """
    Add a new task to the database.
    Returns the ID of the newly created task.
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, description) VALUES (?, ?)',
            (title, description)
        )
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error adding task: {e}")
        return None

def get_all_tasks(include_completed=False):
    """
    Retrieve all tasks from the database.
    If include_completed is False, only returns active tasks.
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        if include_completed:
            cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        else:
            cursor.execute('SELECT * FROM tasks WHERE completed = 0 ORDER BY created_at DESC')
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching tasks: {e}")
        return []

def get_task(task_id):
    """
    Retrieve a single task by its ID.
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error fetching task {task_id}: {e}")
        return None

def update_task(task_id, title=None, description=None, completed=None):
    """
    Update task details.
    Only updates the fields that are provided (not None).
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if title is not None:
            updates.append("title = ?")
            params.append(title)
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        if completed is not None:
            updates.append("completed = ?")
            params.append(completed)
        
        if not updates:
            return False  # Nothing to update
        
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        params.append(task_id)
        
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating task {task_id}: {e}")
        return False

def delete_task(task_id):
    """
    Delete a task from the database.
    Returns True if the task was deleted, False otherwise.
    """
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting task {task_id}: {e}")
        return False

def mark_task_completed(task_id):
    """
    Mark a task as completed.
    """
    return update_task(task_id, completed=True)

def mark_task_active(task_id):
    """
    Mark a task as active (not completed).
    """
    return update_task(task_id, completed=False)
```

This `db.py` file provides all the necessary database operations for a To-Do List application:

1. Database connection management with connection pooling
2. Initialization of the database schema
3. CRUD operations for tasks (Create, Read, Update, Delete)
4. Specialized functions for marking tasks as completed/active
5. Error handling for database operations
6. Proper connection cleanup

The code follows best practices by:
- Using context managers for database connections
- Parameterized queries to prevent SQL injection
- Proper error handling
- Separation of concerns (only database operations here)
- Clean and documented functions

To use this in your Flask application, you'll need to register the `close_db` function with your app's teardown context.