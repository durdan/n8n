import unittest
from datetime import datetime
from models.user import User
from repositories.user_repository import UserRepository
from services.user_service import UserService
from controllers.user_controller import UserController
from exceptions import UserNotFoundError, UserAlreadyExistsError, InvalidCredentialsError

class TestUserModel(unittest.TestCase):
    def test_valid_user_creation(self):
        user = User(
            id="123",
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            created_at=datetime.now()
        )
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_active)
    
    def test_invalid_username(self):
        with self.assertRaises(ValueError):
            User(
                id="123",
                username="ab",  # Too short
                email="test@example.com",
                password_hash="hashed_password",
                created_at=datetime.now()
            )
    
    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            User(
                id="123",
                username="testuser",
                email="invalid-email",
                password_hash="hashed_password",
                created_at=datetime.now()
            )

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.repository = UserRepository()
        self.service = UserService(self.repository)
    
    def test_create_user_success(self):
        user = self.service.create_user("testuser", "test@example.com", "password123")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
    
    def test_create_user_duplicate_username(self):
        self.service.create_user("testuser", "test1@example.com", "password123")
        
        with self.assertRaises(UserAlreadyExistsError):
            self.service.create_user("testuser", "test2@example.com", "password123")
    
    def test_authenticate_success(self):
        user = self.service.create_user("testuser", "test@example.com", "password123")
        authenticated = self.service.authenticate("testuser", "password123")
        self.assertEqual(authenticated.id, user.id)
    
    def test_authenticate_invalid_password(self):
        self.service.create_user("testuser", "test@example.com", "password123")
        
        with self.assertRaises(InvalidCredentialsError):
            self.service.authenticate("testuser", "wrongpassword")
    
    def test_get_nonexistent_user(self):
        with self.assertRaises(UserNotFoundError):
            self.service.get_user("nonexistent")
    
    def test_password_too_short(self):
        with self.assertRaises(ValueError):
            self.service.create_user("testuser", "test@example.com", "12345")

class TestUserController(unittest.TestCase):
    def setUp(self):
        repository = UserRepository()
        service = UserService(repository)
        self.controller = UserController(service)
    
    def test_create_user_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        result = self.controller.create_user(data)
        self.assertIn('id', result)
        self.assertEqual(result['username'], 'testuser')
    
    def test_create_user_missing_data(self):
        data = {'username': 'testuser'}  # Missing email and password
        result = self.controller.create_user(data)
        self.assertIn('error', result)
    
    def test_authenticate_success(self):
        # Create user first
        create_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        self.controller.create_user(create_data)
        
        # Authenticate
        auth_data = {'username': 'testuser', 'password': 'password123'}
        result = self.controller.authenticate(auth_data)
        self.assertEqual(result['username'], 'testuser')

if __name__ == '__main__':
    unittest.main()