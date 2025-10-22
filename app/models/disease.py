from extensions import db

class Disease(db.Model):
    __tablename__ = 'diseases'

    disease_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100))
    symptoms = db.Column(db.Text)
    treatment = db.Column(db.Text)

    crop_links = db.relationship('CropDisease', back_populates='disease')
    livestock_links = db.relationship('LivestockDisease', back_populates='disease')

    def __repr__(self):
        return f"<Disease {self.name}>"
