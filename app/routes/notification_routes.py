from flask import Blueprint, request, jsonify, abort
from extensions import db
from app.models.notification import Notification

notification_bp = Blueprint('notifications', __name__)

# --- Helper function for secure user retrieval (MOCK/PLACEHOLDER) ---
# NOTE: This MUST be replaced with actual user ID retrieval from your JWT token or session.
def get_current_user_id():
    # TODO: Implement secure user ID retrieval based on your authentication system.
    # We use '1' as a placeholder for the current logged-in user for initial testing.
    return 1 

# --- GET ALL NOTIFICATIONS ---
@notification_bp.route('/', methods=['GET'], strict_slashes=False) 
def get_notifications():
    """Gets all notifications for the current user."""
    user_id = get_current_user_id()
    
    # CRITICAL: Filter notifications only for the current user
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    
    # Using 'n.to_dict()' for each notification item
    return jsonify([n.to_dict() for n in notifications]), 200 ## successful response 

# --- MARK AS READ (FIXED: Accepts PUT method from frontend) ---
@notification_bp.route('/<int:id>/read', methods=['PUT', 'PATCH']) # <-- FIX HERE
def mark_as_read(id):
    """Marks a specific notification as read."""
    user_id = get_current_user_id()
    # SECURITY CHECK: Find the notification by ID AND ensure it belongs to the current user
    notification = Notification.query.filter_by(id=id, user_id=user_id).first()
    
    if notification is None:
        # If the notification doesn't exist or doesn't belong to the user, return 404
        abort(404, description=f"Notification with ID {id} not found for current user.")

    notification.read = True
    db.session.commit()
    
    return jsonify(notification.to_dict()), 200

# --- CREATE NEW NOTIFICATION ---
@notification_bp.route('/', methods=['POST'], strict_slashes=False)
def create_notification():
    """Creates a new notification (typically done by system/admin)."""
    data = request.get_json()
    
    # Validation for system/admin POST
    if 'message' not in data or 'user_id' not in data:
        return jsonify({'message': 'Missing required fields: message and user_id'}), 400
    
    # NOTE: In production, this route MUST be protected by @jwt_required and a role check.
    
    new_notification = Notification( ## new notification 
        user_id=data.get('user_id'), 
        message=data.get('message')
    )
    db.session.add(new_notification)
    db.session.commit()

    print(f"New notification created for user {new_notification.user_id}!")
    return jsonify(new_notification.to_dict()), 201

# --- DELETE NOTIFICATION ---
@notification_bp.route('/<int:id>', methods=['DELETE'])
def delete_notification(id):
    """Deletes a specific notification."""
    user_id = get_current_user_id()
    # SECURITY CHECK: Find and delete the notification only if it belongs to the current user
    notification = Notification.query.filter_by(id=id, user_id=user_id).first()
    
    if notification is None:
        abort(404, description=f"Notification with ID {id} not found for current user.")

    db.session.delete(notification)
    db.session.commit()
    
    return jsonify({'message': f'Notification ID {id} deleted successfully'}), 200