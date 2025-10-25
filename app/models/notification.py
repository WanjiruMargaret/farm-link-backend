from extensions import db
##from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='notifications')

    def __repr__(self):
        return f"<notification {self.type}>"