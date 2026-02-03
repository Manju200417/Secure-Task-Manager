from database import get_db_connection
import logging

logger = logging.getLogger(__name__)

class Task:
    
    @staticmethod
    def create(title, description, user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, description, user_id) VALUES (?, ?, ?)',
            (title, description, user_id)
        )
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        logger.info(f"Task created by user {user_id}: {title}")
        return task_id
    
    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
        tasks = cursor.fetchall()
        conn.close()
        return tasks
    
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        conn.close()
        return tasks
    
    @staticmethod
    def get_by_id(task_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        conn.close()
        return task
    
    @staticmethod
    def update(task_id, title, description):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE tasks SET title = ?, description = ? WHERE id = ?',
            (title, description, task_id)
        )
        conn.commit()
        conn.close()
        logger.info(f"Task {task_id} updated")
    
    @staticmethod
    def delete(task_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        logger.info(f"Task {task_id} deleted")