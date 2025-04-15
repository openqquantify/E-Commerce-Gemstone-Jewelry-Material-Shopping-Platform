import os
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, folder='products'):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(
            current_app.config['UPLOAD_FOLDER'], 
            folder
        )
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save original
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Create thumbnail
        img = Image.open(filepath)
        img.thumbnail((300, 300))
        thumb_path = os.path.join(upload_folder, f"thumb_{filename}")
        img.save(thumb_path)
        
        return filename
    return None
