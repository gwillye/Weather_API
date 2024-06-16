from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    frequency = db.Column(db.String(20), nullable=False)

    def __init__(self, email, frequency):
        self.email = email
        self.frequency = frequency

    def __repr__(self):
        return f'<Subscriber {self.email}>'
