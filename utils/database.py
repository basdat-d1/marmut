import psycopg2
import psycopg2.extras
from django.conf import settings
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    connection = None
    try:
        connection = psycopg2.connect(
            host=settings.DATABASES['default']['HOST'],
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            port=settings.DATABASES['default']['PORT']
        )
        yield connection
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            connection.close()

def execute_query(query, params=None, fetch=True):
    """Execute a SQL query and return results"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, params or [])
            
            if fetch:
                if cursor.description:
                    return cursor.fetchall()
                return []
            else:
                conn.commit()
                return cursor.rowcount

def execute_single_query(query, params=None):
    """Execute a SQL query and return single result"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, params or [])
            return cursor.fetchone()

def execute_insert_query(query, params=None):
    """Execute an INSERT query and return the inserted row"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            try:
                cursor.execute(query + " RETURNING *", params or [])
                conn.commit()
                return cursor.fetchone()
            except psycopg2.IntegrityError as e:
                conn.rollback()
                raise

def execute_update_query(query, params=None):
    """Execute an UPDATE query and return number of affected rows"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or [])
            conn.commit()
            return cursor.rowcount

def execute_delete_query(query, params=None):
    """Execute a DELETE query and return number of affected rows"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or [])
            conn.commit()
            return cursor.rowcount

# Alias functions for backward compatibility
def fetch_one(query, params=None):
    """Alias for execute_single_query"""
    return execute_single_query(query, params)

def fetch_all(query, params=None):
    """Alias for execute_query"""
    return execute_query(query, params) 