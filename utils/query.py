import psycopg2
from django.conf import settings

def get_db_connection():
    return psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT']
    )

def run_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)

        if query.upper().startswith('SELECT'):
            return cursor.fetchall()
        else:
            connection.commit()
    except Exception as e:
        connection.rollback()
        print(e)
    finally:
        cursor.close()
        connection.close()