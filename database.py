import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('task_manager.db')
        return conn
    except Error as e:
        print(e)

def create_tables(conn):
    tasks_table = """
        CREATE TABLE IF NOT EXISTS tasks (
            id integer PRIMARY KEY,
            title text NOT NULL,
            description text,
            category text,
            priority text,
            deadline text,
            completed integer
        );
    """
    try:
        c = conn.cursor()
        c.execute(tasks_table)
    except Error as e:
        print(e)

def insert_task(conn, task):
    sql = '''
        INSERT INTO tasks(title, description, category, priority, deadline, completed)
        VALUES(?,?,?,?,?,0);
    '''
    try:
        c = conn.cursor()
        c.execute(sql, task)
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(e)

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
            completed =?
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