from flask import Blueprint, request, jsonify
from datetime import datetime, date
from .models import User, db

bp = Blueprint('routes', __name__)

@bp.route('/hello/<username>', methods=['PUT'])
def save_user(username):
    if not username.isalpha():
        return "Username must contain only letters.", 400
    data = request.get_json()
    try:
        dob = datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date()
        if dob >= date.today():
            return "Date of birth must be before today.", 400
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD.", 400

    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username, date_of_birth=dob)
        db.session.add(user)
    else:
        user.date_of_birth = dob
    db.session.commit()
    return '', 204

@bp.route('/hello/<username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return "User not found.", 404

    days_to_birthday = User.calculate_days_to_birthday(user.date_of_birth)
    if days_to_birthday == 0:
        message = f"Hello, {username}! Happy birthday!"
    else:
        message = f"Hello, {username}! Your birthday is in {days_to_birthday} day(s)."
    return jsonify({"message": message}), 200
