import re
from typing import List

class UserValidator:
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    @staticmethod
    def validate_username(username: str) -> List[str]:
        errors = []
        if not username or not username.strip():
            errors.append("Username is required")
        elif len(username.strip()) < 3:
            errors.append("Username must be at least 3 characters long")
        elif len(username.strip()) > 50:
            errors.append("Username must be less than 50 characters")
        elif not username.replace('_', '').replace('-', '').isalnum():
            errors.append("Username can only contain letters, numbers, hyphens, and underscores")
        return errors
    
    @staticmethod
    def validate_email(email: str) -> List[str]:
        errors = []
        if not email or not email.strip():
            errors.append("Email is required")
        elif not UserValidator.EMAIL_PATTERN.match(email.strip()):
            errors.append("Invalid email format")
        return errors
    
    @staticmethod
    def validate_password(password: str) -> List[str]:
        errors = []
        if not password:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        elif len(password) > 128:
            errors.append("Password must be less than 128 characters")
        return errors