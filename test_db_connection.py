import psycopg2
import os
from psycopg2 import OperationalError

# Fetch environment variables
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'dpg-cq4c2jdds78s73chu1n0-a')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'local_time_project')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'local_time_project_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'hq66YiC5TBxamPoxdvCS67hR8wnFFsk1')

try:
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB
    )
    cursor = conn.cursor()
    cursor.execute("SELECT current_database()")
    result = cursor.fetchone()
    print(f"Connected to database: {result[0]}")
    cursor.close()
    conn.close()
except OperationalError as e:
    print(f"Error connecting to PostgreSQL: {e}")

