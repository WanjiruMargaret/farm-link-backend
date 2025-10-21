from extensions import db, bcrypt
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50))
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    crops = db.relationship("Crop", backref="user", lazy=True)
    livestock = db.relationship("Livestock", backref="user", lazy=True)
    posts = db.relationship("Post", backref="user", lazy=True)
    notifications = db.relationship("Notification", backref="user", lazy=True)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    def __repr__(self):
        return f"<User {self.email}>"