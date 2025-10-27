from flask import Blueprint, request, jsonify
from app.models.crop import Crop
from extensions import db

crop_bp = Blueprint('crop', __name__)

@crop_bp.route('/', methods=['POST'])
def add_crop():
    try:
        data = request.get_json()
        name = data.get('name')
        planting_season = data.get('planting_season')
        expected_harvest = data.get('expected_harvest')
        current_stage = data.get('stage', 'planted')
        farmer_id = data.get('farmer_id')

        new_crop = Crop(
            name=name,
            planting_season=planting_season,
            expected_harvest=expected_harvest,
            current_stage=current_stage,
            farmer_id=farmer_id
        )
        
        db.session.add(new_crop)
        db.session.commit()
        return jsonify(new_crop.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400 

@crop_bp.route('/', methods=['GET'])
def get_crops():
    crops = Crop.query.all()
    crops_list = [crop.to_dict() for crop in crops]
    return jsonify(crops_list), 200 

@crop_bp.route('/<int:id>', methods=['GET'])
def get_crop(id):
    crop = Crop.query.get_or_404(id)
    return jsonify(crop.to_dict()), 200