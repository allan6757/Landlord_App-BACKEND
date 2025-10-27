# Cloudinary Image Upload Service
# Handles image uploads with resizing and optimization

import os
import cloudinary
import cloudinary.uploader
from PIL import Image
from io import BytesIO

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
    
    def optimize_image(self, image_file, max_width=1200, max_height=1200, quality=85):
        """
        Optimize image before uploading (resize and compress)
        
        Args:
            image_file: File object or file path
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            quality: JPEG quality (1-100)
            
        Returns:
            BytesIO object with optimized image
        """
        try:
            # Open image with PIL
            img = Image.open(image_file)
            
            # Convert RGBA to RGB if necessary (for JPEG)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Calculate new dimensions while maintaining aspect ratio
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Save optimized image to BytesIO
            output = BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            
            return output
            
        except Exception as e:
            print(f"Error optimizing image: {str(e)}")
            return None
    
    def upload_image(self, image_file, folder='rental_platform', public_id=None, optimize=True):
        """
        Upload image to Cloudinary with optional optimization
        
        Args:
            image_file: File object to upload
            folder: Cloudinary folder name
            public_id: Custom public ID for the image
            optimize: Whether to optimize image before upload
            
        Returns:
            Dictionary with image URL and public_id, or None if failed
        """
        # Check if Cloudinary is configured
        if not self.is_configured():
            print("Warning: Cloudinary not configured")
            return None
        
        try:
            # Optimize image before upload if requested
            if optimize:
                optimized_image = self.optimize_image(image_file)
                if optimized_image:
                    image_file = optimized_image
            
            # Upload to Cloudinary
            upload_options = {
                'folder': folder,
                'resource_type': 'image',
                'format': 'jpg'  # Convert all images to JPEG
            }
            
            # Add public_id if provided
            if public_id:
                upload_options['public_id'] = public_id
            
            # Perform upload
            result = cloudinary.uploader.upload(image_file, **upload_options)
            
            # Return image details
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
            public_id=f'property_{property_id}_{os.urandom(4).hex()}',
            optimize=True
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
            public_id=f'user_{user_id}',
            optimize=True
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
