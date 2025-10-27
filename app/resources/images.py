# Image Upload Resources
# Handles image uploads to Cloudinary (Required for Capstone)

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.property import Property
from app.utils.cloudinary_service import cloudinary_service
from app.utils.decorators import landlord_required
from flasgger import swag_from

class UploadPropertyImage(Resource):
    """
    Upload property image to Cloudinary
    """
    
    @jwt_required()
    @landlord_required
    def post(self, property_id):
        """
        Upload image for a property
        ---
        tags:
          - Properties
        security:
          - Bearer: []
        parameters:
          - name: property_id
            in: path
            type: integer
            required: true
            description: ID of the property
          - name: image
            in: formData
            type: file
            required: true
            description: Image file to upload (JPEG, PNG)
        responses:
          200:
            description: Image uploaded successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                image_url:
                  type: string
          400:
            description: No image provided or invalid format
          403:
            description: Not authorized to upload image for this property
          404:
            description: Property not found
        """
        # Check if image file is in request
        if 'image' not in request.files:
            return {'error': 'No image file provided'}, 400
        
        image_file = request.files['image']
        
        # Check if file is selected
        if image_file.filename == '':
            return {'error': 'No image file selected'}, 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        file_ext = image_file.filename.rsplit('.', 1)[1].lower() if '.' in image_file.filename else ''
        
        if file_ext not in allowed_extensions:
            return {'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF'}, 400
        
        try:
            # Get current user
            user_id = get_jwt_identity()
            
            # Get property and verify ownership
            property_obj = Property.query.get_or_404(property_id)
            
            # Check if user owns this property (landlord check)
            if property_obj.landlord_id != user_id:
                return {'error': 'You are not authorized to upload images for this property'}, 403
            
            # Upload image to Cloudinary with optimization
            image_url = cloudinary_service.upload_property_image(
                image_file=image_file,
                property_id=property_id
            )
            
            if not image_url:
                return {'error': 'Failed to upload image. Please try again.'}, 500
            
            # Update property with image URL
            property_obj.image_url = image_url
            db.session.commit()
            
            return {
                'message': 'Image uploaded successfully',
                'image_url': image_url
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': f'Upload failed: {str(e)}'}, 500

class UploadProfileImage(Resource):
    """
    Upload user profile image to Cloudinary
    """
    
    @jwt_required()
    def post(self):
        """
        Upload profile image for current user
        ---
        tags:
          - Users
        security:
          - Bearer: []
        parameters:
          - name: image
            in: formData
            type: file
            required: true
            description: Profile image file (JPEG, PNG)
        responses:
          200:
            description: Profile image uploaded successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                image_url:
                  type: string
          400:
            description: No image provided or invalid format
        """
        # Check if image file is in request
        if 'image' not in request.files:
            return {'error': 'No image file provided'}, 400
        
        image_file = request.files['image']
        
        # Check if file is selected
        if image_file.filename == '':
            return {'error': 'No image file selected'}, 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        file_ext = image_file.filename.rsplit('.', 1)[1].lower() if '.' in image_file.filename else ''
        
        if file_ext not in allowed_extensions:
            return {'error': 'Invalid file type. Allowed: PNG, JPG, JPEG'}, 400
        
        try:
            # Get current user
            user_id = get_jwt_identity()
            user = User.query.get_or_404(user_id)
            
            # Upload image to Cloudinary with optimization
            image_url = cloudinary_service.upload_profile_image(
                image_file=image_file,
                user_id=user_id
            )
            
            if not image_url:
                return {'error': 'Failed to upload image. Please try again.'}, 500
            
            # Update user profile with image URL
            if user.profile:
                # Add profile_image_url field if it doesn't exist
                # This would require a migration to add the column
                # For now, we'll just return the URL
                pass
            
            return {
                'message': 'Profile image uploaded successfully',
                'image_url': image_url
            }, 200
            
        except Exception as e:
            return {'error': f'Upload failed: {str(e)}'}, 500
