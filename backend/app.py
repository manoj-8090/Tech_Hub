import os
from pathlib import Path
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

from config import Config
from database import init_db
from routes.auth_routes import auth_bp
from routes.search_routes import search_bp

# Define frontend path with multi-location fallback
FRONTEND_DIR = Path(__file__).resolve().parent.parent / 'frontend'
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = Path(__file__).resolve().parent / 'frontend'
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = Path(os.getcwd()) / 'frontend'

def create_app():
    app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path='')
    app.config.from_object(Config)

    # Enable CORS for cross-origin frontend requests
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize SQLite database
    init_db()

    # Register API Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy', 'service': 'TechHub API', 'version': '1.0.0'}), 200

    # Serve Frontend Pages & Static Assets
    @app.route('/')
    def serve_index():
        return send_from_directory(str(FRONTEND_DIR), 'index.html')

    @app.route('/<path:filename>')
    def serve_static(filename):
        target = FRONTEND_DIR / filename
        if target.exists():
            return send_from_directory(str(FRONTEND_DIR), filename)
        # Fallback to index if route not found
        return send_from_directory(str(FRONTEND_DIR), 'index.html')

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    is_debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1']
    print(f"🚀 TechHub Server running at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=is_debug)
