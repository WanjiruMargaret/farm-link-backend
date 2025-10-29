from extensions import db
##from datetime import datetime

class Market(db.Model):
    __tablename__ = 'market'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Available')
    image_url = db.Column(db.String, nullable=True)

    # FIX: The foreign key must reference 'users.user_id'
    seller_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)


    seller = db.relationship('User', back_populates='market_items')

    def __repr__(self):
        return f"<market {self.type}>"