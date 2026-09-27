import sys
import os
from pathlib import Path

# Add backend directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / 'backend'
sys.path.insert(0, str(BACKEND_DIR))

try:
    from app import create_app
except ImportError as e:
    print("Missing required Python dependencies. Please run:")
    print("pip install -r backend/requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app = create_app()
    print("=" * 65)
    print("  TECHHUB: Multi-Source Technical Q&A with Consensus Detection")
    print("=" * 65)
    print(f"  ➜ Server running locally at: http://localhost:{port}")
    print(f"  ➜ API Health Check:         http://localhost:{port}/health")
    print("=" * 65)
    app.run(host='0.0.0.0', port=port, debug=True)
