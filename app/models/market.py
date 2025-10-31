from extensions import db
from datetime import datetime # Required for timestamp column

class Market(db.Model):
    __tablename__ = 'market'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Available')
    description = db.Column(db.Text, nullable=True) # Added description field for marketplace listings
    image_url = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Added creation timestamp

    # FIX: The foreign key must reference 'users.user_id' (assuming your User model's ID column is named 'user_id')
    seller_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True) 

    # Relationship setup (assuming your User model has 'market_items' set as back_populates)
    seller = db.relationship('User', back_populates='market_items')

    def __repr__(self):
        return f"<Market {self.name} ({self.type}) - ${self.price}>"

    # CRITICAL FIX: This method is mandatory for your route to return JSON successfully.
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'price': self.price,
            'status': self.status,
            'description': self.description,
            'image_url': self.image_url,
            'seller_id': self.seller_id,
            # Ensure datetime objects are converted to a serializable string (ISO format)
            'created_at': self.created_at.isoformat() if self.created_at else None 
        }
