from dataclasses import dataclass
from typing import Optional
import re
from datetime import datetime

@dataclass
class User:
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True
    
    def __post_init__(self):
        self._validate()
    
    def _validate(self):
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters")
        
        if not self._is_valid_email(self.email):
            raise ValueError("Invalid email format")
        
        if not self.username.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Username can only contain letters, numbers, hyphens, and underscores")
    
    def _is_valid_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None