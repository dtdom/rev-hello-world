from .database import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    @staticmethod
    def calculate_days_to_birthday(dob):
        today = date.today()
        next_birthday = dob.replace(year=today.year)
        if today > next_birthday:
            next_birthday = dob.replace(year=today.year + 1)
        return (next_birthday - today).days