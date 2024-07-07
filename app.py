from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import socket
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

class LocalTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    local_time = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return "Welcome to the Local Time Project API!"

@app.route('/test_db_connection')
def test_db_connection():
    try:
        host = app.config['POSTGRES_HOST']
        ip = socket.gethostbyname(host)
        app.logger.info(f"Resolved {host} to {ip}")
        with db.engine.connect() as connection:
            result = connection.execute("SELECT 1")
            return f"Database connection successful. Resolved IP: {ip}", 200
    except socket.gaierror as e:
        return f"Error resolving hostname: {str(e)}", 500
    except SQLAlchemyError as e:
        return f"Error connecting to PostgreSQL: {str(e)}", 500
    except Exception as e:
        return f"Unexpected error: {str(e)}", 500

@app.route('/api/localtime', methods=['POST'])
def local_time():
    data = request.get_json()
    local_time = data.get('localTime')
    if local_time:
        new_local_time = LocalTime(local_time=local_time)
        try:
            db.session.add(new_local_time)
            db.session.commit()
            return jsonify({"message": f"Received local time: {local_time}"}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": f"Error saving to database: {str(e)}"}), 500
    else:
        return jsonify({"error": "No local time provided"}), 400

@app.route('/api/localtime', methods=['GET'])
def get_local_times():
    try:
        local_times = LocalTime.query.all()
        result = [
            {"id": lt.id, "local_time": lt.local_time, "timestamp": lt.timestamp} 
            for lt in local_times
        ]
        return jsonify(result), 200
    except SQLAlchemyError as e:
        return jsonify({"error": f"Error retrieving from database: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

