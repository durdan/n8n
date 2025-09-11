from typing import Dict, List, Optional
from user_model import User

class UserRepository:
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._username_index: Dict[str, str] = {}  # username -> user_id
        self._email_index: Dict[str, str] = {}     # email -> user_id
    
    def save(self, user: User) -> None:
        self._users[user.id] = user
        self._username_index[user.username.lower()] = user.id
        self._email_index[user.email.lower()] = user.id
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def find_by_username(self, username: str) -> Optional[User]:
        user_id = self._username_index.get(username.lower())
        return self._users.get(user_id) if user_id else None
    
    def find_by_email(self, email: str) -> Optional[User]:
        user_id = self._email_index.get(email.lower())
        return self._users.get(user_id) if user_id else None
    
    def find_all(self) -> List[User]:
        return list(self._users.values())
    
    def delete(self, user_id: str) -> bool:
        user = self._users.get(user_id)
        if not user:
            return False
        
        del self._users[user_id]
        del self._username_index[user.username.lower()]
        del self._email_index[user.email.lower()]
        return True
    
    def update(self, user: User) -> None:
        old_user = self._users.get(user.id)
        if old_user:
            # Update indexes if username or email changed
            if old_user.username.lower() != user.username.lower():
                del self._username_index[old_user.username.lower()]
                self._username_index[user.username.lower()] = user.id
            
            if old_user.email.lower() != user.email.lower():
                del self._email_index[old_user.email.lower()]
                self._email_index[user.email.lower()] = user.id
        
        self._users[user.id] = user
    
    def exists_username(self, username: str, exclude_user_id: Optional[str] = None) -> bool:
        user_id = self._username_index.get(username.lower())
        return user_id is not None and user_id != exclude_user_id
    
    def exists_email(self, email: str, exclude_user_id: Optional[str] = None) -> bool:
        user_id = self._email_index.get(email.lower())
        return user_id is not None and user_id != exclude_user_id