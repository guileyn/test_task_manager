# database.py
import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('task_manager.db')
        create_tables(conn)
        return conn
    except Error as e:
        print(e)

def create_tables(conn):
    tasks_table = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL UNIQUE,
            description TEXT,
            category TEXT,
            priority TEXT,
            deadline DATE,
            completed INTEGER,
            completed_date DATE,
            creation_date DATE
        );
    """
    try:
        c = conn.cursor()
        c.execute(tasks_table)
        print("Tasks table created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")

def insert_task(conn, task):
    sql = '''
        INSERT INTO tasks(title, description, category, priority, deadline, completed, completed_date, creation_date)
        VALUES(?,?,?,?,?,0,0,DATE('now'));
    '''
    try:
        c = conn.cursor()
        c.execute(sql, task)
        conn.commit()
        print(f"Task '{task[0]}' inserted with creation date.")
        return c.lastrowid
    except sqlite3.IntegrityError as e:  # Catch IntegrityError, which happens on UNIQUE constraint violation
        print(f"Error: A task with the title '{task[0]}' already exists.")
        return None
    except Error as e:
        print(f"Error inserting task: {e}")
        return None

def select_all_tasks(conn):
    sql = "SELECT * FROM tasks"
    try:
        c = conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        return rows
    except Error as e:
        print(e)

def update_task(conn, task):
    sql = '''
        UPDATE tasks
        SET title =?,
            description =?,
            category =?,
            priority =?,
            deadline =?,
            completed =?,
            completed_date =?
        WHERE id =?
    '''
    try:
        c = conn.cursor()
        c.execute(sql, task)
        conn.commit()
    except Error as e:
        print(e)

def delete_task(conn, task_id):
    sql = 'DELETE FROM tasks WHERE id = ?'
    try:
        c = conn.cursor()
        c.execute(sql, (task_id,))
        conn.commit()
        print(f"Task with ID {task_id} deleted successfully.")
    except Error as e:
        print(f"Error deleting the task: {e}")

def mark_task_completed(conn, date, task_id):
    sql = '''
        UPDATE tasks
        SET completed = 1,
            completed_date = ?
        WHERE id = ?
    '''
    try:
        c = conn.cursor()
        c.execute(sql, (date, task_id,))
        conn.commit()
        print(f"Task with ID {task_id} marked as completed.")
    except Error as e:
        print(f"Error marking task as completed: {e}")
