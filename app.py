import psutil
import logging
import os
import jwt
from flask import Flask, jsonify, request, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime, timedelta

app = Flask(__name__)

# Security setup: Using JWT for authentication
SECRET_KEY = 'your-very-secret-key'
JWT_ALGORITHM = 'HS256'

# Logger setup
logging.basicConfig(filename='api_monitor.log', level=logging.INFO)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def log_activity(action, status):
    logging.info(f"{datetime.now()} - Action: {action} - Status: {status}")

def authenticate_request():
    token = request.headers.get('Authorization', None)
    if not token:
        abort(403)  # Forbidden if no token
    try:
        jwt.decode(token.split("Bearer ")[-1], SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        abort(401)  # Unauthorized if token expired
    except jwt.InvalidTokenError:
        abort(401)  # Unauthorized if token is invalid

@app.route('/cpu', methods=['GET'])
@limiter.limit("10 per minute")
def get_cpu_usage():
    authenticate_request()
    cpu_usage = psutil.cpu_percent()
    log_activity('CPU Usage Check', 'Success')
    return jsonify({'cpu_usage': str(cpu_usage) + " %"}), 200

@app.route('/memory', methods=['GET'])
@limiter.limit("10 per minute")
def get_memory_usage():
    authenticate_request()
    memory = psutil.virtual_memory()
    log_activity('Memory Usage Check', 'Success')
    return jsonify({
        "total": str(int(psutil.virtual_memory().total/(1024 ** 2))) + " MB",
        "available": str(int(psutil.virtual_memory().available/(1024 ** 2))) + " MB",
        "percent": str(psutil.virtual_memory().percent) + " %",
        "used": str(int(psutil.virtual_memory().used/(1024 ** 2))) + " MB",
        "free": str(int(psutil.virtual_memory().free/(1024 ** 2))) + " MB"
    }), 200

@app.route('/disk', methods=['GET'])
@limiter.limit("10 per minute")
def get_disk_usage():
    authenticate_request()
    disk = psutil.disk_usage('/')
    log_activity('Disk Usage Check', 'Success')
    return jsonify({
        "total": str(int(disk.total/(1024 ** 3))) + " GB",
        "percent": str(disk.percent) + " %",
        "used": str(int(disk.used/(1024 ** 3))) + " GB",
        "free": str(int(disk.free/(1024 ** 3))) + " GB"
    }), 200

@app.route('/bandwidth', methods=['GET'])
@limiter.limit("10 per minute")
def get_bandwidth_usage():
    authenticate_request()
    net_io = psutil.net_io_counters()
    bandwidth_used = {
        'bytes_sent': str(net_io.bytes_sent) + " bytes",
        'bytes_received': str(net_io.bytes_recv) + " bytes"
    }
    log_activity('Bandwidth Usage Check', 'Success')
    return jsonify({'bandwidth_usage': bandwidth_used}), 200

# Token generator for testing
@app.route('/token', methods=['GET'])
@limiter.limit("10 per minute")
def get_token():
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({'exp': expiration}, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return jsonify({'token': token})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
