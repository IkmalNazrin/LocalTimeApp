import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL configurations from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

