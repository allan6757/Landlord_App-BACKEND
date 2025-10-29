import cloudinary
import cloudinary.uploader
from flask import current_app

def init_cloudinary():
    """Initialize Cloudinary with error handling"""
    try:
        cloudinary.config(
            cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=current_app.config['CLOUDINARY_API_KEY'],
            api_secret=current_app.config['CLOUDINARY_API_SECRET']
        )
        return True
    except Exception as e:
        current_app.logger.error(f"Cloudinary config error: {e}")
        return False

def upload_image(file, folder="properties"):
    """Upload image to Cloudinary with error handling"""
    try:
        if not current_app.config.get('CLOUDINARY_CLOUD_NAME'):
            return {'error': 'Cloudinary not configured'}
            
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="image",
            transformation=[
                {'width': 800, 'height': 600, 'crop': 'fill'},
                {'quality': 'auto:good'}
            ]
        )
        return {
            'url': result['secure_url'],
            'public_id': result['public_id']
        }
    except Exception as e:
        current_app.logger.error(f"Cloudinary upload error: {e}")
        return {'error': f'Upload failed: {str(e)}'}

def delete_image(public_id):
    """Delete image from Cloudinary with error handling"""
    try:
        if not current_app.config.get('CLOUDINARY_CLOUD_NAME'):
            return False
            
        result = cloudinary.uploader.destroy(public_id)
        return result.get('result') == 'ok'
    except Exception as e:
        current_app.logger.error(f"Cloudinary delete error: {e}")
        return False