from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import cloudinary.uploader 
import cloudinary
import os

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
@upload_bp.route('/test', methods=['GET'])
def test_cloudinary():
    try:
        from cloudinary.api import ping
        result = ping()
        return jsonify({"status": "success", "result": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

