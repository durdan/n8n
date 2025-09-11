from typing import Dict, Optional, List
from models.user import User
from exceptions import UserNotFoundError, UserAlreadyExistsError

class UserRepository:
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._username_index: Dict[str, str] = {}
        self._email_index: Dict[str, str] = {}
    
    def save(self, user: User) -> User:
        if user.id in self._users:
            # Update existing user
            old_user = self._users[user.id]
            self._remove_from_indexes(old_user)
        else:
            # Check for conflicts
            if user.username in self._username_index:
                raise UserAlreadyExistsError(f"Username '{user.username}' already exists")
            if user.email in self._email_index:
                raise UserAlreadyExistsError(f"Email '{user.email}' already exists")
        
        self._users[user.id] = user
        self._username_index[user.username] = user.id
        self._email_index[user.email] = user.id
        return user
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def find_by_username(self, username: str) -> Optional[User]:
        user_id = self._username_index.get(username)
        return self._users.get(user_id) if user_id else None
    
    def find_by_email(self, email: str) -> Optional[User]:
        user_id = self._email_index.get(email)
        return self._users.get(user_id) if user_id else None
    
    def delete(self, user_id: str) -> bool:
        user = self._users.get(user_id)
        if not user:
            return False
        
        self._remove_from_indexes(user)
        del self._users[user_id]
        return True
    
    def list_all(self) -> List[User]:
        return list(self._users.values())
    
    def _remove_from_indexes(self, user: User):
        self._username_index.pop(user.username, None)
        self._email_index.pop(user.email, None)