from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    description = db.Column(db.String(100))
    temp = db.Column(db.Float)
    feels_like = db.Column(db.Float)
    temp_min = db.Column(db.Float)
    temp_max = db.Column(db.Float)
    pressure = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    visibility = db.Column(db.Integer)
    wind_speed = db.Column(db.Float)
    wind_deg = db.Column(db.Integer)
    clouds_all = db.Column(db.Integer)
    sunrise = db.Column(db.Integer)
    sunset = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'lon': self.lon,
            'lat': self.lat,
            'description': self.description,
            'temp': self.temp,
            'feels_like': self.feels_like,
            'temp_min': self.temp_min,
            'temp_max': self.temp_max,
            'pressure': self.pressure,
            'humidity': self.humidity,
            'visibility': self.visibility,
            'wind_speed': self.wind_speed,
            'wind_deg': self.wind_deg,
            'clouds_all': self.clouds_all,
            'sunrise': self.sunrise,
            'sunset': self.sunset
        }
