from database import get_db_connection
from utils.auth_helper import hash_password, check_password
import logging
import sqlite3

logger = logging.getLogger(__name__)

class User:
    
    @staticmethod
    def create(name, email, password, role='user'):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            hashed_pw = hash_password(password)
            cursor.execute(
                'INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)',
                (name, email, hashed_pw, role)
            )
            conn.commit()
            user_id = cursor.lastrowid
            logger.info(f"New user registered: {email}")
            return user_id
        except sqlite3.IntegrityError:
            logger.warning(f"Registration failed - email already exists: {email}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def find_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, role FROM users')
        users = cursor.fetchall()
        conn.close()
        return users
    
    @staticmethod
    def delete(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        logger.info(f"User {user_id} deleted")