from flask import Blueprint, request, jsonify
from extensions import db
from app.models.market import Market
from app.models.user import User 
# Assuming you have a Livestock model defined elsewhere:
from app.models.livestock import Livestock 
from sqlalchemy import or_

market_bp = Blueprint('market', __name__)

# --- READ ALL MARKET ITEMS ---
@market_bp.route('/', methods=['GET'], strict_slashes=False)
def get_market_items():
    """Fetches all general market items."""
    try:
        items = Market.query.all() 
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        # Better error logging for the 500 error you saw previously
        print(f"Error fetching market items: {e}")
        return jsonify({"message": "Server error fetching general market items."}), 500

# --- CREATE NEW ITEM ---
@market_bp.route('/', methods=['POST'], strict_slashes=False)
def market_item():
    """Creates a new market listing."""
    data = request.get_json() 
    if not data.get('name') or not data.get('price') or not data.get('seller_id'):
        return jsonify({"message": "Name, price, and seller_id are required for a new market item."}), 400
        
    try:
        new_item = Market(
            name=data.get('name'),
            price=data.get('price'),
            location=data.get('location'),
            seller_id=data.get('seller_id'),
            description=data.get('description', '')
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.to_dict()), 201
    except Exception as e:
        print(f"Error creating market item: {e}")
        return jsonify({"message": "Server error creating market item."}), 500

# --- UPDATE ITEM STATUS (or other fields) ---
@market_bp.route('/<int:id>', methods=['PATCH'])
def update_status(id):
    """Updates the status or other fields of a market item."""
    item = Market.query.get_or_404(id)
    data = request.get_json()
    
    item.status = data.get('status', item.status)
    item.price = data.get('price', item.price)
    item.description = data.get('description', item.description)

    db.session.commit()
    return jsonify(item.to_dict()), 200

# --- DELETE ITEM ---
@market_bp.route('/<int:id>', methods=['DELETE'])
def delete_item(id):
    """Deletes a market item."""
    item = Market.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully.'}), 200

# --- LIVESTOCK LISTINGS ROUTE (FIXED) ---
@market_bp.route('/livestock', methods=['GET'])
def get_public_livestock_listings():
    """
    Fetches all items marked as 'Livestock' (or related type) by joining Market and User tables.
    
    NOTE: We simplify the join. Instead of joining Market to Livestock and then to User, 
    we join Market directly to User using the foreign key Market.seller_id.
    We filter by items that have 'livestock' in their 'type' column.
    """
    search_term = request.args.get('search', '').lower()
    location_filter = request.args.get('location')

    try:
        # Query Market items where type is 'Livestock' and join directly to User
        query = db.session.query(Market, User).join(
            User,
            Market.seller_id == User.user_id
        ).filter(
            Market.type.ilike('%livestock%')
        )
        
        if search_term:
            query = query.filter(
                or_(
                    Market.name.ilike(f'%{search_term}%'),  
                    Market.description.ilike(f'%{search_term}%')
                )
            )
            
        if location_filter:
            # Assuming User model has a location field. If Market has its own, use that.
            query = query.filter(User.location.ilike(f'%{location_filter}%'))

        listings = query.all()
        
        out = []
        for market_item, user_item in listings:
            # We map the combined result to a structured dictionary
            out.append({
                "id": market_item.id,
                "name": market_item.name,
                "type": market_item.type,
                "location": market_item.location or user_item.location or "Unknown Region", 
                "price": market_item.price, 
                "status": market_item.status,
                "description": market_item.description,
                "seller": user_item.fullName if hasattr(user_item, 'fullName') else user_item.username, 
                "seller_id": market_item.seller_id,
                "image_url": market_item.image_url
            })
            
        return jsonify(out), 200
    except Exception as e:
        # Catch and log the specific Python exception causing the 500 error
        print(f"CRITICAL 500 ERROR in /api/market/livestock: {e}")
        # Return a custom 500 response so the frontend knows what happened
        return jsonify({
            "message": "Internal Server Error. Check server logs for database or model relationship errors."
        }), 500