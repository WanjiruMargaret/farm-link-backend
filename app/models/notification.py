from extensions import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.String(500), nullable=False) ## a notification, or alert messange
    read = db.Column(db.Boolean, default=False) ## when the user reads, mark it read 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    user = db.relationship('User', backref='notifications')

    def to_dict(self):
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'read': self.read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


    def __repr__(self):
        return f"<notification {self.type}>"