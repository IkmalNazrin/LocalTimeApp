from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import logging
import pymysql
from sqlalchemy import text

# Register pymysql as MySQLdb
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://starlight:St%40rLight1@localhost/local_time_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/localtime', methods=['GET', 'POST'])
def receive_local_time():
    if request.method == 'POST':
        try:
            data = request.json
            received_time = data['localTime']
            
            logging.debug("Attempting to connect to MySQL...")
            try:
                conn = db.engine.connect()
                if conn is None:
                    logging.error("MySQL connection is None")
                    return jsonify({"error": "MySQL connection is None"}), 500
                logging.debug("MySQL connection established")
                conn.execute(text("INSERT INTO time_functions (function_name, last_updated) VALUES (:function_name, :last_updated)"),
                             {'function_name': 'send_local_time', 'last_updated': received_time})
            except Exception as e:
                logging.error(f"Unexpected error when connecting to MySQL: {str(e)}")
                return jsonify({"error": f"Unexpected error when connecting to MySQL: {str(e)}"}), 500
            
            logging.debug("Executing SQL query...")
            conn.close()
            
            return jsonify({"message": "Time received and stored successfully"})
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    else:  # GET request
        return jsonify({"message": "Send a POST request with localTime to store the time"})

@app.route('/test_db_connection')
def test_db_connection():
    try:
        logging.debug("Attempting to connect to MySQL in test_db_connection")
        conn = db.engine.connect()
        if conn is None:
            logging.error("MySQL connection is None")
            return "MySQL connection is None", 500
        result = conn.execute(text("SELECT DATABASE()"))
        db_name = result.fetchone()
        conn.close()
        return f"Connected to database: {db_name[0]}", 200
    except Exception as e:
        logging.error(f"Error connecting to MySQL: {str(e)}")
        return f"Error connecting to MySQL: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

