from extensions import db

class Weather(db.Model):
    __tablename__ = 'weather'

    weather_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    temperature = db.Column(db.Numeric(5, 2))
    humidity = db.Column(db.Numeric(5, 2))
    rainfall = db.Column(db.Numeric(5, 2))
    wind_speed = db.Column(db.Numeric(5, 2))
    condition = db.Column(db.String(100))
    date_recorded = db.Column(db.Date)

    def __repr__(self):
        return f"<Weather {self.condition}>"
