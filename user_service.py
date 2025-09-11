import hashlib
import uuid
from datetime import datetime
from typing import List, Optional
from user_model import User
from user_repository import UserRepository
from user_validator import UserValidator

class UserServiceError(Exception):
    pass

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.validator = UserValidator()
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        return self._hash_password(password) == password_hash
    
    def create_user(self, username: str, email: str, password: str) -> User:
        # Validate input
        errors = []
        errors.extend(self.validator.validate_username(username))
        errors.extend(self.validator.validate_email(email))
        errors.extend(self.validator.validate_password(password))
        
        if errors:
            raise UserServiceError(f"Validation failed: {'; '.join(errors)}")
        
        # Check uniqueness
        username = username.strip()
        email = email.strip()
        
        if self.repository.exists_username(username):
            raise UserServiceError("Username already exists")
        
        if self.repository.exists_email(email):
            raise UserServiceError("Email already exists")
        
        # Create user
        user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            password_hash=self._hash_password(password),
            created_at=datetime.now(),
            is_active=True
        )
        
        self.repository.save(user)
        return user
    
    def authenticate_user(self, username_or_email: str, password: str) -> Optional[User]:
        if not username_or_email or not password:
            return None
        
        # Try to find by username first, then email
        user = self.repository.find_by_username(username_or_email)
        if not user:
            user = self.repository.find_by_email(username_or_email)
        
        if user and user.is_active and self._verify_password(password, user.password_hash):
            return user
        
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.repository.find_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.repository.find_by_username(username)
    
    def get_all_users(self) -> List[User]:
        return self.repository.find_all()
    
    def update_user(self, user_id: str, username: Optional[str] = None, 
                   email: Optional[str] = None, password: Optional[str] = None) -> User:
        user = self.repository.find_by_id(user_id)
        if not user:
            raise UserServiceError("User not found")
        
        # Validate updates
        errors = []
        if username is not None:
            username = username.strip()
            errors.extend(self.validator.validate_username(username))
            if self.repository.exists_username(username, exclude_user_id=user_id):
                errors.append("Username already exists")
        
        if email is not None:
            email = email.strip()
            errors.extend(self.validator.validate_email(email))
            if self.repository.exists_email(email, exclude_user_id=user_id):
                errors.append("Email already exists")
        
        if password is not None:
            errors.extend(self.validator.validate_password(password))
        
        if errors:
            raise UserServiceError(f"Validation failed: {'; '.join(errors)}")
        
        # Update user
        updated_user = User(
            id=user.id,
            username=username if username is not None else user.username,
            email=email if email is not None else user.email,
            password_hash=self._hash_password(password) if password is not None else user.password_hash,
            created_at=user.created_at,
            is_active=user.is_active
        )
        
        self.repository.update(updated_user)
        return updated_user
    
    def deactivate_user(self, user_id: str) -> bool:
        user = self.repository.find_by_id(user_id)
        if not user:
            return False
        
        if not user.is_active:
            return True
        
        deactivated_user = User(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            is_active=False
        )
        
        self.repository.update(deactivated_user)
        return True
    
    def activate_user(self, user_id: str) -> bool:
        user = self.repository.find_by_id(user_id)
        if not user:
            return False
        
        if user.is_active:
            return True
        
        activated_user = User(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            is_active=True
        )
        
        self.repository.update(activated_user)
        return True
    
    def delete_user(self, user_id: str) -> bool:
        return self.repository.delete(user_id)