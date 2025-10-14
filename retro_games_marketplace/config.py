# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DATABASE_NAME = 'retro_games_marketplace'
    
    # Image upload settings
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}