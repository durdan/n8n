from typing import Dict, Any, List
from services.user_service import UserService
from exceptions import UserManagementError

class UserController:
    def __init__(self, user_service: UserService):
        self._user_service = user_service
    
    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            if not all([username, email, password]):
                return {'error': 'Username, email, and password are required'}
            
            user = self._user_service.create_user(username, email, password)
            return self._user_to_dict(user)
            
        except UserManagementError as e:
            return {'error': str(e)}
        except ValueError as e:
            return {'error': str(e)}
    
    def authenticate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            if not all([username, password]):
                return {'error': 'Username and password are required'}
            
            user = self._user_service.authenticate(username, password)
            return self._user_to_dict(user)
            
        except UserManagementError as e:
            return {'error': str(e)}
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        try:
            user = self._user_service.get_user(user_id)
            return self._user_to_dict(user)
        except UserManagementError as e:
            return {'error': str(e)}
    
    def list_users(self) -> Dict[str, Any]:
        try:
            users = self._user_service.list_users()
            return {'users': [self._user_to_dict(user) for user in users]}
        except UserManagementError as e:
            return {'error': str(e)}
    
    def _user_to_dict(self, user) -> Dict[str, Any]:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'is_active': user.is_active
        }