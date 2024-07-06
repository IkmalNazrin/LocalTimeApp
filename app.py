from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)

# PostgreSQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://local_time_project_user:hq66YiC5TBxamPoxdvCS67hR8wnFFsk1@dpg-cq4c2jdd578s73chuln0-a:5432/local_time_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/api/localtime', methods=['GET', 'POST'])
def receive_local_time():
    if request.method == 'POST':
        try:
            data = request.json
            received_time = data['localTime']

            print("Attempting to connect to PostgreSQL...", file=sys.stderr)
            try:
                conn = db.engine.connect()
                if conn is None:
                    print("PostgreSQL connection is None", file=sys.stderr)
                    return jsonify({"error": "PostgreSQL connection is None"}), 500
                print("PostgreSQL connection established", file=sys.stderr)
            except Exception as e:
                print(f"Unexpected error when connecting to PostgreSQL: {str(e)}", file=sys.stderr)
                return jsonify({"error": f"Unexpected error when connecting to PostgreSQL: {str(e)}"}), 500

            print("Executing SQL query...", file=sys.stderr)
            conn.execute("INSERT INTO time_functions (function_name, last_updated) VALUES (%s, %s)", ('send_local_time', received_time))
            conn.close()

            return jsonify({"message": "Time received and stored successfully"})
        except Exception as e:
            print(f"Unexpected error: {str(e)}", file=sys.stderr)
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    else:  # GET request
        return jsonify({"message": "Send a POST request with localTime to store the time"})

@app.route('/test_db_connection')
def test_db_connection():
    try:
        conn = db.engine.connect()
        if conn is None:
            return "PostgreSQL connection is None", 500
        result = conn.execute("SELECT current_database()")
        db_name = result.fetchone()
        conn.close()
        return f"Connected to database: {db_name[0]}", 200
    except Exception as e:
        return f"Error connecting to PostgreSQL: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

