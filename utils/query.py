from functools import wraps
from django.db import connection

def connectdb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with connection.cursor() as cursor:
            # cursor.execute("SET search_path to MARMUT;")
            return func(cursor, *args, **kwargs)
        
    return wrapper