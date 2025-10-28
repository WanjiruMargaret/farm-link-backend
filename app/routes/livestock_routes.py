from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from app.models.livestock import Livestock
from app.models.relations import LivestockDisease
from app.models.disease import Disease

livestock_bp = Blueprint("livestock", __name__)

# Create livestock
@livestock_bp.route("/", methods=["POST"])
@jwt_required()
def create_livestock():
    identity = get_jwt_identity()
    user_id = identity.get("id")

    data = request.get_json()
    type_ = data.get("type")
    health_status = data.get("health_status")
    image_url = data.get("image_url")
    disease_ids = data.get("disease_ids", [])

    if not type_:
        return jsonify({"error": "Type is required"}), 400

    animal = Livestock(user_id=user_id, type=type_, health_status=health_status, image_url=image_url)
    db.session.add(animal)
    db.session.flush()

    for d_id in disease_ids:
        disease = Disease.query.get(d_id)
        if disease:
            db.session.add(LivestockDisease(livestock_id=animal.livestock_id, disease_id=d_id))

    db.session.commit()
    return jsonify({"message": "Livestock created", "livestock_id": animal.livestock_id}), 201

# List livestock for user or admin
@livestock_bp.route("/", methods=["GET"])
@jwt_required()
def list_livestock():
    identity = get_jwt_identity()
    user_id = identity.get("id")
    role = identity.get("role")

    if role == "admin":
        items = Livestock.query.all()
    else:
        items = Livestock.query.filter_by(user_id=user_id).all()

    out = []
    for a in items:
        out.append({
            "livestock_id": a.livestock_id,
            "user_id": a.user_id,
            "type": a.type,
            "health_status": a.health_status,
            "image_url": a.image_url
        })
    return jsonify(out), 200

# Get single
@livestock_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_livestock(id):
    item = Livestock.query.get_or_404(id)
    return jsonify({
        "livestock_id": item.livestock_id,
        "user_id": item.user_id,
        "type": item.type,
        "health_status": item.health_status,
        "image_url": item.image_url
    }), 200

# Update
@livestock_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_livestock(id):
    identity = get_jwt_identity()
    user_id = identity.get("id")
    role = identity.get("role")

    animal = Livestock.query.get_or_404(id)
    if animal.user_id != user_id and role != "admin":
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    animal.type = data.get("type", animal.type)
    animal.health_status = data.get("health_status", animal.health_status)
    animal.image_url = data.get("image_url", animal.image_url)

    disease_ids = data.get("disease_ids")
    if disease_ids is not None:
        LivestockDisease.query.filter_by(livestock_id=animal.livestock_id).delete()
        for d_id in disease_ids:
            db.session.add(LivestockDisease(livestock_id=animal.livestock_id, disease_id=d_id))

    db.session.commit()
    return jsonify({"message": "Livestock updated"}), 200

# Delete
@livestock_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_livestock(id):
    identity = get_jwt_identity()
    user_id = identity.get("id")
    role = identity.get("role")

    animal = Livestock.query.get_or_404(id)
    if animal.user_id != user_id and role != "admin":
        return jsonify({"error": "Forbidden"}), 403

    LivestockDisease.query.filter_by(livestock_id=animal.livestock_id).delete()
    db.session.delete(animal)
    db.session.commit()
    return jsonify({"message": "Livestock deleted"}), 200
