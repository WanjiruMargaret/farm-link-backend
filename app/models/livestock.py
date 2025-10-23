from extensions import db

class Livestock(db.Model):
    __tablename__ = 'livestock'

    livestock_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    type = db.Column(db.String(100))
    health_status = db.Column(db.String(100))
    image_url = db.Column(db.String(255))

    diseases = db.relationship('LivestockDisease', back_populates='livestock')

    def __repr__(self):
        return f"<Livestock {self.type}>"
