from flask import Blueprint, request, jsonify
from app.models.disease import Disease
from extensions import db

disease_bp = Blueprint('disease', __name__)

## Get all diseases
@disease_bp.route('/', methods=['GET'])
def get_diseases():
    disease = disease.quesry.all()

    return jsonify(new_disease.to_dict()) 200

### post 