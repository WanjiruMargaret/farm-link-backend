from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from app.models.weather import Weather

weather_bp = Blueprint("weather", __name__)

# Create weather record (user-specific)
@weather_bp.route("/", methods=["POST"])
@jwt_required()
def create_weather():
    identity = get_jwt_identity()
    user_id = identity.get("id")

    data = request.get_json()
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    rainfall = data.get("rainfall")
    wind_speed = data.get("wind_speed")
    condition = data.get("condition")
    date_recorded = data.get("date_recorded")  # expect 'YYYY-MM-DD' or None

    weather = Weather(
        user_id=user_id,
        temperature=temperature,
        humidity=humidity,
        rainfall=rainfall,
        wind_speed=wind_speed,
        condition=condition,
        date_recorded=date_recorded
    )
    db.session.add(weather)
    db.session.commit()
    return jsonify({"message": "Weather record added", "weather_id": weather.weather_id}), 201

# Get weather records for user (or admin all)
@weather_bp.route("/", methods=["GET"])
@jwt_required()
def list_weather():
    identity = get_jwt_identity()
    user_id = identity.get("id")
    role = identity.get("role")

    if role == "admin":
        records = Weather.query.all()
    else:
        records = Weather.query.filter_by(user_id=user_id).all()

    out = []
    for r in records:
        out.append({
            "weather_id": r.weather_id,
            "user_id": r.user_id,
            "temperature": str(r.temperature) if r.temperature is not None else None,
            "humidity": str(r.humidity) if r.humidity is not None else None,
            "rainfall": str(r.rainfall) if r.rainfall is not None else None,
            "wind_speed": str(r.wind_speed) if r.wind_speed is not None else None,
            "condition": r.condition,
            "date_recorded": r.date_recorded.isoformat() if r.date_recorded else None
        })
    return jsonify(out), 200

# Update weather
@weather_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_weather(id):
    identity = get_jwt_identity()
    user_id = identity.get("id")
    role = identity.get("role")

    rec = Weather.query.get_or_404(id)
    if rec.user_id != user_id and role != "admin":
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    rec.temperature = data.get("temperature", rec.temperature)
    rec.humidity = data.get("humidity", rec.humidity)
    rec.rainfall = data.get("rainfall", rec.rainfall)
    rec.wind_speed = data.get("wind_speed", rec.wind_speed)
    rec.condition = data.get("condition", rec.condition)
    rec.date_recorded = data.get("date_recorded", rec.date_recorded)

    db.session.commit()
    return jsonify({"message": "Weather updated"}), 200

# Delete
@weather_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_weather(id):
    identity = get_jwt_identity()
    user_id = identity.get("id")
    role = identity.get("role")

    rec = Weather.query.get_or_404(id)
    if rec.user_id != user_id and role != "admin":
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(rec)
    db.session.commit()
    return jsonify({"message": "Weather record deleted"}), 200
