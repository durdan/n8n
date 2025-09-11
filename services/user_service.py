import hashlib
import secrets
from typing import Optional
from models.user import User
from repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def create_user(self, username: str, email: str, password: str) -> User:
        # Check for existing users
        if self.user_repo.get_by_username(username):
            raise ValueError("Username already exists")
        
        if self.user_repo.get_by_email(email):
            raise ValueError("Email already exists")
        
        # Validate password strength
        self._validate_password(password)
        
        # Hash password
        password_hash = self._hash_password(password)
        
        user = User(
            id=None,
            username=username,
            email=email,
            password_hash=password_hash
        )
        
        return self.user_repo.create(user)
    
    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_username(username)
        if not user or not user.is_active:
            return None
        
        if self._verify_password(password, user.password_hash):
            return user
        
        return None
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repo.get_by_id(user_id)
    
    def update_user(self, user_id: int, username: str = None, 
                   email: str = None, password: str = None) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if username and username != user.username:
            if self.user_repo.get_by_username(username):
                raise ValueError("Username already exists")
            user.username = username
        
        if email and email != user.email:
            if self.user_repo.get_by_email(email):
                raise ValueError("Email already exists")
            user.email = email
        
        if password:
            self._validate_password(password)
            user.password_hash = self._hash_password(password)
        
        return self.user_repo.update(user)
    
    def deactivate_user(self, user_id: int) -> bool:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        self.user_repo.update(user)
        return True
    
    def _validate_password(self, password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one digit")
    
    def _hash_password(self, password: str) -> str:
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        return f"{salt}:{password_hash.hex()}"
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        try:
            salt, hash_hex = stored_hash.split(':')
            password_hash = hashlib.pbkdf2_hmac('sha256',
                                              password.encode('utf-8'),
                                              salt.encode('utf-8'),
                                              100000)
            return secrets.compare_digest(hash_hex, password_hash.hex())
        except ValueError:
            return False