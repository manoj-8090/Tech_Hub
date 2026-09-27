import os
from pathlib import Path
from flask import Flask, send_from_directory, jsonify, request
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

ALLOWED_ORIGINS = [
    "https://tech-hub-nine.vercel.app",
    "https://tech-hub-1-vc99.onrender.com",
    "http://localhost:5000",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:3000"
]

def create_app():
    app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path='')
    app.config.from_object(Config)

    # Enable Flask-CORS for all routes
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Global preflight OPTIONS handler for all endpoints
    @app.before_request
    def handle_preflight():
        if request.method == "OPTIONS":
            response = app.make_default_options_response()
            origin = request.headers.get("Origin")
            if origin and (origin in ALLOWED_ORIGINS or origin.endswith(".vercel.app") or origin.endswith(".onrender.com")):
                response.headers["Access-Control-Allow-Origin"] = origin
            else:
                response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept"
            response.headers["Access-Control-Max-Age"] = "3600"
            return response

    # Global response header injector for CORS
    @app.after_request
    def set_cors_headers(response):
        origin = request.headers.get("Origin")
        if origin and (origin in ALLOWED_ORIGINS or origin.endswith(".vercel.app") or origin.endswith(".onrender.com")):
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With, Accept"
        return response

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
