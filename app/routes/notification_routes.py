from flask import Blueprint, request, jsonify
from extensions import db
from app.models.notification import Notification

notification_bp = Blueprint('notifications', __name__)

@notification_bp.route('/', methods=['GET']) ## get all the notifications
def get_notifications():
    notifications = Notification.query.order_by(Notification.created_at.desc()).all() ## show the latest notification(newest)to pop 
    
    return jsonify([n.to_dict() for n in notifications]), 200 ## successful responce 

@notification_bp.route('/<int:id>/read', methods=['PATCH'])
def mark_as_read(id):
    # Find the notification by its ID, or return 404 if not found
    notification = Notification.query.get_or_404(id)
    notification.read = True
    db.session.commit()
    
    return jsonify(notification.to_dict()), 200

@notification_bp.route('/', methods=['POST'])
def create_notification():
    data = request.get_json()
    new_notification = Notification( ## new notification 
        message=data.get('message')
    )
    db.session.add(new_notification)
    db.session.commit()

    
    print("You have a new notification!") ## this will help the user to know of any notifications 

    return jsonify(new_notification.to_dict()), 201


@notification_bp.route('/<int:id>', methods=['DELETE'])
def delete_notification(id):
    notification = Notification.query.get_or_404(id)

    db.session.delete(notification)
    db.session.commit()
    
    return jsonify({'message': f'Notification ID {id} deleted successfully'}), 200
