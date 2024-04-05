from flask_testing import TestCase
from app import app
import pytest

class TestRoutes(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_home(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assertEqual(response.data, b'Hello there!')

    def test_get_user(self):
        response = self.client.get('/user/1')
        self.assert200(response)

    def test_update_user(self):
        response = self.client.put('/user/1', json={'name': 'new name'})
        self.assert200(response)

    def test_delete_user(self):
        response = self.client.delete('/user/1')
        self.assert200(response)

    def test_get_user_listings(self):
        response = self.client.get('/user/1/listings')
        self.assert200(response)

    def test_app_feedback(self):
        response = self.client.post('/app/feedback', json={'feedback': 'Great app!'})
        self.assert200(response)

    def test_product(self):
        response = self.client.get('/product/1')
        self.assert200(response)

    def test_create_product(self):
        response = self.client.post('/product/create/addToDb', json={
            'prod_title': 'Test Product',
            'description': 'This is a test product',
            'prod_condition': 'new',
            'listed_price': 100,
            'quantity': 1,
            'category': 'electronics',
            'sub_category': 'laptop'
        })
        self.assert201(response)

    def test_create_chat(self):
        response = self.client.post('/chat', json={
            'message_id': 1,
            'sender_id': 1,
            'prod_id': 1
        })
        self.assert201(response)

    def test_get_chat(self):
        response = self.client.get('/chat/1')
        self.assert200(response)

    def test_delete_chat(self):
        response = self.client.delete('/chat/1')
        self.assert200(response)

    def test_signup(client):
        response = client.post('/signup', data={
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'phone_no': '1234567890',
            'gender': 'Male',
            'residence_location': 'Test Location',
            'residence_number': '123',
            'anonymity_level': 'High',
            'theme_preference': 'Dark',
            'language_preference': 'English',
            'notification_preference': 'Email'
        })
        assert response.status_code == 302  # Redirect to login page

    def test_login(client):
        response = client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        assert response.status_code == 302  # Redirect to home page

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello there!'

# def test_create_chat(client):
#     response = client.post('/chat', json={
#         'message_id': 1,
#         'sender_id': 1,
#         'prod_id': 1
#     })
#     assert response.status_code == 201

# def test_get_chat(client):
#     response = client.get('/chat/1')
#     assert response.status_code == 200

# def test_delete_chat(client):
#     response = client.delete('/chat/1')
#     assert response.status_code == 200