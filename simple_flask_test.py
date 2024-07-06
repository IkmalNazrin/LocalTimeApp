from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'starlight'
app.config['MYSQL_PASSWORD'] = 'St@rLight1'
app.config['MYSQL_DB'] = 'local_time_db'

mysql = MySQL(app)

@app.route('/test_db_connection')
def test_db_connection():
    try:
        conn = mysql.connection
        if conn is None:
            return "MySQL connection is None", 500
        cur = conn.cursor()
        cur.execute("SELECT DATABASE()")
        db_name = cur.fetchone()
        cur.close()
        return f"Connected to database: {db_name[0]}", 200
    except Exception as e:
        return f"Error connecting to MySQL: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

