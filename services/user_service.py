import hashlib
import uuid
from datetime import datetime
from typing import Optional, List
from models.user import User
from repositories.user_repository import UserRepository
from exceptions import UserNotFoundError, InvalidCredentialsError

class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository
    
    def create_user(self, username: str, email: str, password: str) -> User:
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        
        user_id = str(uuid.uuid4())
        password_hash = self._hash_password(password)
        
        user = User(
            id=user_id,
            username=username.strip(),
            email=email.strip().lower(),
            password_hash=password_hash,
            created_at=datetime.now()
        )
        
        return self._repository.save(user)
    
    def authenticate(self, username: str, password: str) -> User:
        user = self._repository.find_by_username(username)
        if not user or not user.is_active:
            raise InvalidCredentialsError("Invalid username or password")
        
        if not self._verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid username or password")
        
        return user
    
    def get_user(self, user_id: str) -> User:
        user = self._repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id '{user_id}' not found")
        return user
    
    def update_user(self, user_id: str, username: Optional[str] = None, 
                   email: Optional[str] = None) -> User:
        user = self.get_user(user_id)
        
        if username:
            user.username = username.strip()
        if email:
            user.email = email.strip().lower()
        
        # Re-validate after updates
        user._validate()
        return self._repository.save(user)
    
    def deactivate_user(self, user_id: str) -> User:
        user = self.get_user(user_id)
        user.is_active = False
        return self._repository.save(user)
    
    def delete_user(self, user_id: str) -> bool:
        if not self._repository.find_by_id(user_id):
            raise UserNotFoundError(f"User with id '{user_id}' not found")
        return self._repository.delete(user_id)
    
    def list_users(self) -> List[User]:
        return self._repository.list_all()
    
    def _hash_password(self, password: str) -> str:
        # Simple hash for demo - use bcrypt/scrypt in production
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        return self._hash_password(password) == password_hash