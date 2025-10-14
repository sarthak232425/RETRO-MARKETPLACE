# utils/image_utils.py
import os
from PIL import Image
import secrets

class ImageHandler:
    def __init__(self):
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        self.max_size_mb = 5  # Reduced for safety
    
    def allowed_file(self, filename):
        if not filename:
            return False
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def generate_filename(self, original_filename):
        random_hex = secrets.token_hex(8)
        _, ext = os.path.splitext(original_filename)
        return random_hex + ext.lower()
    
    def save_image(self, image_file):
        """Save image and create thumbnail, return (filename, error_message)"""
        if not image_file or not image_file.filename:
            return None, "No file selected"
            
        if not self.allowed_file(image_file.filename):
            return None, "File type not allowed. Use: PNG, JPG, GIF, WebP"
        
        try:
            # Generate secure filename
            filename = self.generate_filename(image_file.filename)
            
            # Define paths
            game_path = os.path.join('static/uploads/games', filename)
            thumb_path = os.path.join('static/uploads/thumbnails', filename)
            
            # Save original image
            image = Image.open(image_file)
            image.save(game_path)
            
            # Create thumbnail
            thumb_size = (300, 300)
            image.thumbnail(thumb_size)
            image.save(thumb_path)
            
            return filename, None
            
        except Exception as e:
            return None, f"Error processing image: {str(e)}"

# Global instance
image_handler = ImageHandler()