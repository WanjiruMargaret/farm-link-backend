from flask import Blueprint, request, jsonify
from extensions import db
from app.models.market import Market

market_bp = Blueprint('market', __name__)

@market_bp.route('/', methods=['GET'])
def get_market_items():
    items = Market.query.all() ## fetch all data from DB
    return jsonify([item.to_dict() for item in items]), 200

@market_bp.route('/', methods=['POST'])
def market_item():
    data = request.get_json() ## read jyson from the frontend
    new_item = Market(
        name=data.get('name'),
        price=data.get('price')
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@market_bp.route('/<int:id>', methods=['PATCH'])
def update_status(id):
    item = Market.query.get_or_404(id)
    data = request.get_json()
    item.status = data.get('status', item.status)
    db.session.commit()
    return jsonify(item.to_dict()), 200

@market_bp.route('/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Market.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 200
