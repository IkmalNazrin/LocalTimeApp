from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import socket

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Welcome to the Local Time Project API!"

@app.route('/test_db_connection')
def test_db_connection():
    try:
        # Try to resolve the hostname
        host = app.config['POSTGRES_HOST']
        ip = socket.gethostbyname(host)
        app.logger.info(f"Resolved {host} to {ip}")
        
        # Test database connection
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
        return jsonify({"message": f"Received local time: {local_time}"}), 200
    else:
        return jsonify({"error": "No local time provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)

