from functools import wraps
from django.db import connection

def connectdb(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = ""
        with connection.cursor() as cursor:
            res = func(cursor, *args, **kwargs)
            
        return res
    return wrapper