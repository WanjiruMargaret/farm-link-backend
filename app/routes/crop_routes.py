from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from app.models.crop import Crop
from app.models.relations import CropDisease
from app.models.disease import Disease

crop_bp = Blueprint("crop", __name__)

# Create crop
@crop_bp.route("/", methods=["POST"])
@jwt_required()
def create_crop():
    identity = get_jwt_identity()  # {"id": user_id, "role": ...}
    user_id = identity.get("id")

    data = request.get_json()
    name = data.get("name")
    type_ = data.get("type")
    health_status = data.get("health_status")
    image_url = data.get("image_url")
    disease_ids = data.get("disease_ids", [])  # optional list of disease ids

    if not name:
        return jsonify({"error": "Name is required"}), 400

    crop = Crop(user_id=user_id, name=name, type=type_, health_status=health_status, image_url=image_url)
    db.session.add(crop)
    db.session.flush()  # get crop.crop_id

    # Link diseases if provided
    for d_id in disease_ids:
        disease = Disease.query.get(d_id)
        if disease:
            link = CropDisease(crop_id=crop.crop_id, disease_id=d_id)
            db.session.add(link)

    db.session.commit()
    return jsonify({"message": "Crop created", "crop_id": crop.crop_id}), 201

# Get all crops for current user (or all if admin)
@crop_bp.route("/", methods=["GET"])
@jwt_required()
def list_crops():
    identity = get_jwt_identity()
    user_id = identity.get("id")
    role = identity.get("role")

    if role == "admin":
        crops = Crop.query.all()
    else:
        crops = Crop.query.filter_by(user_id=user_id).all()

    result = []
    for c in crops:
        result.append({
            "crop_id": c.crop_id,
            "user_id": c.user_id,
            "name": c.name,
            "type": c.type,
            "health_status": c.health_status,
            "image_url": c.image_url
        })
    return jsonify(result), 200

# Get single crop
@crop_bp.route("/<int:crop_id>", methods=["GET"])
@jwt_required()
def get_crop(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    return jsonify({
        "crop_id": crop.crop_id,
        "user_id": crop.user_id,
        "name": crop.name,
        "type": crop.type,
        "health_status": crop.health_status,
        "image_url": crop.image_url
    }), 200

# Update crop
@crop_bp.route("/<int:crop_id>", methods=["PUT"])
@jwt_required()
def update_crop(crop_id):
    identity = get_jwt_identity()
    user_id = identity.get("id")
    role = identity.get("role")

    crop = Crop.query.get_or_404(crop_id)

    # Only owner or admin can update
    if crop.user_id != user_id and role != "admin":
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    crop.name = data.get("name", crop.name)
    crop.type = data.get("type", crop.type)
    crop.health_status = data.get("health_status", crop.health_status)
    crop.image_url = data.get("image_url", crop.image_url)

    # Optionally update disease links (replace with provided list)
    disease_ids = data.get("disease_ids")
    if disease_ids is not None:
        # remove existing links
        CropDisease.query.filter_by(crop_id=crop.crop_id).delete()
        for d_id in disease_ids:
            db.session.add(CropDisease(crop_id=crop.crop_id, disease_id=d_id))

    db.session.commit()
    return jsonify({"message": "Crop updated"}), 200

# Delete crop
@crop_bp.route("/<int:crop_id>", methods=["DELETE"])
@jwt_required()
def delete_crop(crop_id):
    identity = get_jwt_identity()
    user_id = identity.get("id")
    role = identity.get("role")

    crop = Crop.query.get_or_404(crop_id)

    if crop.user_id != user_id and role != "admin":
        return jsonify({"error": "Forbidden"}), 403

    # delete relationships then crop
    CropDisease.query.filter_by(crop_id=crop.crop_id).delete()
    db.session.delete(crop)
    db.session.commit()
    return jsonify({"message": "Crop deleted"}), 200
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from app.models.crop import Crop
from app.models.relations import CropDisease
from app.models.disease import Disease


crop_bp = Blueprint("crop", __name__)

# Create crop

@crop_bp.route("/", methods=["POST"])

@jwt_required()

def create_crop():

    identity = get_jwt_identity()  # {"id": user_id, "role": ...}

    user_id = identity.get("id")



    data = request.get_json()

    name = data.get("name")

    type_ = data.get("type")

    health_status = data.get("health_status")

    image_url = data.get("image_url")

    disease_ids = data.get("disease_ids", [])  # optional list of disease ids



    if not name:

        return jsonify({"error": "Name is required"}), 400



    crop = Crop(user_id=user_id, name=name, type=type_, health_status=health_status, image_url=image_url)

    db.session.add(crop)

    db.session.flush()  # get crop.crop_id



    # Link diseases if provided

    for d_id in disease_ids:

        disease = Disease.query.get(d_id)

        if disease:

            link = CropDisease(crop_id=crop.crop_id, disease_id=d_id)

            db.session.add(link)



    db.session.commit()

    return jsonify({"message": "Crop created", "crop_id": crop.crop_id}), 201



# Get all crops for current user (or all if admin)

@crop_bp.route("/", methods=["GET"])

@jwt_required()

def list_crops():

    identity = get_jwt_identity()

    user_id = identity.get("id")

    role = identity.get("role")



    if role == "admin":

        crops = Crop.query.all()

    else:

        crops = Crop.query.filter_by(user_id=user_id).all()



    result = []

    for c in crops:

        result.append({

            "crop_id": c.crop_id,

            "user_id": c.user_id,

            "name": c.name,

            "type": c.type,

            "health_status": c.health_status,

            "image_url": c.image_url

        })

    return jsonify(result), 200



# Get single crop

@crop_bp.route("/<int:crop_id>", methods=["GET"])

@jwt_required()

def get_crop(crop_id):

    crop = Crop.query.get_or_404(crop_id)

    return jsonify({

        "crop_id": crop.crop_id,

        "user_id": crop.user_id,

        "name": crop.name,

        "type": crop.type,

        "health_status": crop.health_status,

        "image_url": crop.image_url

    }), 200



# Update crop

@crop_bp.route("/<int:crop_id>", methods=["PUT"])

@jwt_required()

def update_crop(crop_id):

    identity = get_jwt_identity()

    user_id = identity.get("id")

    role = identity.get("role")



    crop = Crop.query.get_or_404(crop_id)



    # Only owner or admin can update

    if crop.user_id != user_id and role != "admin":

        return jsonify({"error": "Forbidden"}), 403



    data = request.get_json()

    crop.name = data.get("name", crop.name)

    crop.type = data.get("type", crop.type)

    crop.health_status = data.get("health_status", crop.health_status)

    crop.image_url = data.get("image_url", crop.image_url)



    # Optionally update disease links (replace with provided list)

    disease_ids = data.get("disease_ids")

    if disease_ids is not None:

        # remove existing links

        CropDisease.query.filter_by(crop_id=crop.crop_id).delete()

        for d_id in disease_ids:

            db.session.add(CropDisease(crop_id=crop.crop_id, disease_id=d_id))



    db.session.commit()

    return jsonify({"message": "Crop updated"}), 200



# Delete crop

@crop_bp.route("/<int:crop_id>", methods=["DELETE"])

@jwt_required()

def delete_crop(crop_id):

    identity = get_jwt_identity()

    user_id = identity.get("id")

    role = identity.get("role")



    crop = Crop.query.get_or_404(crop_id)



    if crop.user_id != user_id and role != "admin":

        return jsonify({"error": "Forbidden"}), 403



    # delete relationships then crop

    CropDisease.query.filter_by(crop_id=crop.crop_id).delete()

    db.session.delete(crop)

    db.session.commit()

    return jsonify({"message": "Crop deleted"}), 200

