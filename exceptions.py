class UserManagementError(Exception):
    """Base exception for user management operations"""
    pass

class UserNotFoundError(UserManagementError):
    """Raised when user is not found"""
    pass

class UserAlreadyExistsError(UserManagementError):
    """Raised when trying to create a user that already exists"""
    pass

class InvalidCredentialsError(UserManagementError):
    """Raised when authentication fails"""
    pass