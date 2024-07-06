from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config  # Import the Config class

app = Flask(__name__)
app.config.from_object(Config)  # Load configurations from Config class

db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Welcome to the Local Time Project API!"

@app.route('/test_db_connection')
def test_db_connection():
    try:
        conn = db.engine.connect()
        result = conn.execute("SELECT current_database()")
        db_name = result.fetchone()
        conn.close()
        return f"Connected to database: {db_name[0]}", 200
    except Exception as e:
        return f"Error connecting to PostgreSQL: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

