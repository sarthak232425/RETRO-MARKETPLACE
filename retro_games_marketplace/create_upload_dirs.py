# create_upload_dirs.py
import os

def create_upload_dirs():
    """Create necessary upload directories"""
    directories = [
        'static/uploads/games',
        'static/uploads/thumbnails'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

if __name__ == "__main__":
    create_upload_dirs()