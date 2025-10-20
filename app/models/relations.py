from app import db

class CropDisease(db.Model):
    __tablename__ = 'crop_diseases'

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.crop_id'))
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.disease_id'))

    crop = db.relationship('Crop', back_populates='diseases')
    disease = db.relationship('Disease', back_populates='crop_links')

class LivestockDisease(db.Model):
    __tablename__ = 'livestock_diseases'

    id = db.Column(db.Integer, primary_key=True)
    livestock_id = db.Column(db.Integer, db.ForeignKey('livestock.livestock_id'))
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.disease_id'))

    livestock = db.relationship('Livestock', back_populates='diseases')
    disease = db.relationship('Disease', back_populates='livestock_links')
