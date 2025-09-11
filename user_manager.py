from typing import List, Optional
from user_model import User
from user_repository import UserRepository
from user_service import UserService, UserServiceError

class UserManager:
    def __init__(self):
        self.repository = UserRepository()
        self.service = UserService(self.repository)
    
    def register_user(self, username: str, email: str, password: str) -> dict:
        try:
            user = self.service.create_user(username, email, password)
            return {
                'success': True,
                'user': user.to_dict(),
                'message': 'User created successfully'
            }
        except UserServiceError as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to create user'
            }
    
    def login(self, username_or_email: str, password: str) -> dict:
        user = self.service.authenticate_user(username_or_email, password)
        if user:
            return {
                'success': True,
                'user': user.to_dict(),
                'message': 'Login successful'
            }
        else:
            return {
                'success': False,
                'error': 'Invalid credentials or inactive user',
                'message': 'Login failed'
            }
    
    def get_user_profile(self, user_id: str) -> dict:
        user = self.service.get_user_by_id(user_id)
        if user:
            return {
                'success': True,
                'user': user.to_dict()
            }
        else:
            return {
                'success': False,
                'error': 'User not found'
            }
    
    def update_user_profile(self, user_id: str, **updates) -> dict:
        try:
            user = self.service.update_user(user_id, **updates)
            return {
                'success': True,
                'user': user.to_dict(),
                'message': 'User updated successfully'
            }
        except UserServiceError as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to update user'
            }
    
    def list_users(self) -> dict:
        users = self.service.get_all_users()
        return {
            'success': True,
            'users': [user.to_dict() for user in users],
            'count': len(users)
        }
    
    def deactivate_user(self, user_id: str) -> dict:
        success = self.service.deactivate_user(user_id)
        if success:
            return {
                'success': True,
                'message': 'User deactivated successfully'
            }
        else:
            return {
                'success': False,
                'error': 'User not found',
                'message': 'Failed to deactivate user'
            }
    
    def activate_user(self, user_id: str) -> dict:
        success = self.service.activate_user(user_id)
        if success:
            return {
                'success': True,
                'message': 'User activated successfully'
            }
        else:
            return {
                'success': False,
                'error': 'User not found',
                'message': 'Failed to activate user'
            }
    
    def delete_user(self, user_id: str) -> dict:
        success = self.service.delete_user(user_id)
        if success:
            return {
                'success': True,
                'message': 'User deleted successfully'
            }
        else:
            return {
                'success': False,
                'error': 'User not found',
                'message': 'Failed to delete user'
            }