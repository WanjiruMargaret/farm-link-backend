from extensions import db

class Crop(db.Model):
    __tablename__ = 'crops'

    crop_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100))
    health_status = db.Column(db.String(100))
    image_url = db.Column(db.String(255))

    diseases = db.relationship('CropDisease', back_populates='crop')

    def __repr__(self):
        return f"<Crop {self.name}>"
