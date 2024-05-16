from functools import wraps
from django.db import connection

def connectdb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with connection.cursor() as cursor:
            # cursor.execute("SET search_path to MARMUT;")
            return func(cursor, *args, **kwargs)
        
    return wrapper

# def get_db_connection():
#     return psycopg2.connect(
#         dbname=settings.DATABASES['default']['NAME'],
#         user=settings.DATABASES['default']['USER'],
#         password=settings.DATABASES['default']['PASSWORD'],
#         host=settings.DATABASES['default']['HOST'],
#         port=settings.DATABASES['default']['PORT']
#     )

# def run_query(query, params=None):
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     try:
#         cursor.execute(query, params)

#         if query.upper().startswith('SELECT'):
#             return cursor.fetchall()
#         else:
#             connection.commit()
#     except Exception as e:
#         connection.rollback()
#         return str(e)
#     finally:
#         cursor.close()
#         connection.close()