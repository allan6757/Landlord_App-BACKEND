# Cloudinary Image Upload Service
# Handles image uploads with resizing and optimization

import os
import cloudinary
import cloudinary.uploader

class CloudinaryService:
    """
    Service class for handling image uploads to Cloudinary
    """
    
    def __init__(self):
        # Configure Cloudinary with credentials from environment
        cloudinary.config(
            cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
            api_key=os.environ.get('CLOUDINARY_API_KEY'),
            api_secret=os.environ.get('CLOUDINARY_API_SECRET')
        )
        
    def is_configured(self):
        """Check if Cloudinary is properly configured"""
        return all([
            os.environ.get('CLOUDINARY_CLOUD_NAME'),
            os.environ.get('CLOUDINARY_API_KEY'),
            os.environ.get('CLOUDINARY_API_SECRET')
        ])
    

    
    def upload_image(self, image_file, folder='rental_platform', public_id=None):
        """
        Upload image to Cloudinary
        
        Args:
            image_file: File object to upload
            folder: Cloudinary folder name
            public_id: Custom public ID for the image
            
        Returns:
            Dictionary with image URL and public_id, or None if failed
        """
        if not self.is_configured():
            print("Warning: Cloudinary not configured")
            return None
        
        try:
            upload_options = {
                'folder': folder,
                'resource_type': 'image',
                'transformation': [{'width': 1200, 'height': 1200, 'crop': 'limit', 'quality': 'auto'}]
            }
            
            if public_id:
                upload_options['public_id'] = public_id
            
            result = cloudinary.uploader.upload(image_file, **upload_options)
            
            return {
                'url': result.get('secure_url'),
                'public_id': result.get('public_id'),
                'width': result.get('width'),
                'height': result.get('height'),
                'format': result.get('format')
            }
            
        except Exception as e:
            print(f"Error uploading to Cloudinary: {str(e)}")
            return None
    
    def upload_property_image(self, image_file, property_id):
        """
        Upload property image with specific naming convention
        
        Args:
            image_file: File object to upload
            property_id: ID of the property
            
        Returns:
            Image URL or None
        """
        result = self.upload_image(
            image_file=image_file,
            folder='rental_platform/properties',
            public_id=f'property_{property_id}_{os.urandom(4).hex()}'
        )
        
        return result.get('url') if result else None
    
    def upload_profile_image(self, image_file, user_id):
        """
        Upload user profile image
        
        Args:
            image_file: File object to upload
            user_id: ID of the user
            
        Returns:
            Image URL or None
        """
        result = self.upload_image(
            image_file=image_file,
            folder='rental_platform/profiles',
            public_id=f'user_{user_id}'
        )
        
        return result.get('url') if result else None
    
    def delete_image(self, public_id):
        """
        Delete image from Cloudinary
        
        Args:
            public_id: Public ID of the image to delete
            
        Returns:
            Boolean indicating success
        """
        if not self.is_configured():
            return False
        
        try:
            result = cloudinary.uploader.destroy(public_id)
            return result.get('result') == 'ok'
        except Exception as e:
            print(f"Error deleting image: {str(e)}")
            return False

# Create a singleton instance
cloudinary_service = CloudinaryService()
