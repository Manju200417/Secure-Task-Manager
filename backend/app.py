from flask import Flask, jsonify
from flask_cors import CORS
from database import init_database
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from config import Config
import logging
import os

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

# Initialize database
init_database()

# Register blueprints with versioning
app.register_blueprint(auth_bp, url_prefix='/api/v1')
app.register_blueprint(tasks_bp, url_prefix='/api/v1/tasks')

# Basic route
@app.route('/')
def home():
    return jsonify({'message': 'Backend API is running'}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(debug=True, port=5000)