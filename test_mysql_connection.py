import MySQLdb

try:
    conn = MySQLdb.connect(
        host='localhost',
        user='starlight',
        password='St@rLight1',
        database='local_time_db'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE()")
    result = cursor.fetchone()
    print(f"Connected to database: {result}")
    cursor.close()
    conn.close()
except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")

