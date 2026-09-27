import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'techhub-super-secret-key-change-in-production-2026')
    JWT_SECRET = os.environ.get('JWT_SECRET', 'techhub-jwt-secret-key-2026')
    JWT_EXPIRATION_HOURS = int(os.environ.get('JWT_EXPIRATION_HOURS', 24))
    
    # SQLite file path
    DB_PATH = os.environ.get('DATABASE_PATH', str(BASE_DIR / 'techhub.db'))
    
    # Optional external API keys (intelligent fallbacks operate if not set)
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
    
    # Timeout for external HTTP scrapers/APIs (seconds)
    API_TIMEOUT = int(os.environ.get('API_TIMEOUT', 6))
