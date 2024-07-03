import unittest
from app import create_app
from app.database import db
from app.models import User
from datetime import datetime, timedelta, date

class HelloWorldTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_save_user(self):
        response = self.client.put('/hello/testuser', json={'dateOfBirth': '2000-01-01'})
        self.assertEqual(response.status_code, 204)
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.date_of_birth.strftime('%Y-%m-%d'), '2000-01-01')

    def test_save_user_invalid_username(self):
        response = self.client.put('/hello/testuser123', json={'dateOfBirth': '2000-01-01'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username must contain only letters.', response.data.decode())

    def test_save_user_invalid_date_format(self):
        response = self.client.put('/hello/testuser', json={'dateOfBirth': '01-01-2000'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid date format. Use YYYY-MM-DD.', response.data.decode())

    def test_save_user_date_not_before_today(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        response = self.client.put('/hello/testuser', json={'dateOfBirth': future_date})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Date of birth must be before today.', response.data.decode())

    def test_get_user_birthday_message(self):
        dob = datetime.now().date() - timedelta(days=1)
        user = User(username='testuser', date_of_birth=dob)
        db.session.add(user)
        db.session.commit()
        response = self.client.get('/hello/testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your birthday is in', response.json['message'])

    def test_get_user_birthday_today_message(self):
        dob = datetime.now().date()
        user = User(username='testuser', date_of_birth=dob)
        db.session.add(user)
        db.session.commit()
        response = self.client.get('/hello/testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Happy birthday!', response.json['message'])

    def test_get_user_not_found(self):
        response = self.client.get('/hello/nonexistentuser')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found.', response.data.decode())

if __name__ == '__main__':
    unittest.main()
