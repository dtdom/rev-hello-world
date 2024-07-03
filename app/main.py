from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import re

# Initialize Flask app and configure database settings
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Create database tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

# Endpoint to add or update a user
@app.route('/hello/<username>', methods=['PUT'])
def add_or_update_user(username):
    if not re.match("^[a-zA-Z]+$", username):
        abort(400, "Username must contain only letters.")
    data = request.get_json()
    date_of_birth = data.get('dateOfBirth')
    try:
        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        if date_of_birth >= datetime.now().date():
            abort(400, "Date of birth must be before today's date.")
    except ValueError:
        abort(400, "Invalid date format. Use YYYY-MM-DD.")

    user = User.query.filter_by(username=username).first()
    if user:
        user.date_of_birth = date_of_birth
    else:
        user = User(username=username, date_of_birth=date_of_birth)
        db.session.add(user)
    db.session.commit()
    return '', 204

# Endpoint to get a birthday message for a user
@app.route('/hello/<username>', methods=['GET'])
def get_birthday_message(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404, "User not found.")
    today = datetime.now().date()
    next_birthday = datetime(today.year, user.date_of_birth.month, user.date_of_birth.day).date()
    if next_birthday < today:
        next_birthday = datetime(today.year + 1, user.date_of_birth.month, user.date_of_birth.day).date()
    days_until_birthday = (next_birthday - today).days

    if days_until_birthday == 0:
        message = f"Hello, {username}! Happy birthday!"
    else:
        message = f"Hello, {username}! Your birthday is in {days_until_birthday} day(s)."
    return jsonify(message=message), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
