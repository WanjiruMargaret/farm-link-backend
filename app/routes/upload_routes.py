from flask import Blueprint, request, jsonify
import cloudinary.uploader

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image = request.files['image']
    
    # Upload to Cloudinary
    result = cloudinary.uploader.upload(image)
    
    return jsonify({
        'url': result['secure_url'], ## give back image url
        'public_id': result['public_id'] ## give back 
    }), 200
