# db_connection.py

import psycopg2
from django.conf import settings

class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=settings.DATABASES['default']['HOST'],
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD']
        )
        self.cursor = self.connection.cursor()

    def execute1(self, query, params=None):
        self.cursor.execute(query, params)
        if self.cursor.description:  
            return self.cursor.fetchall()
        return None 

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()