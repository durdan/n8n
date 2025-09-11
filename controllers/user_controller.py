from flask import Flask, request, jsonify
from services.user_service import UserService
from repositories.user_repository import UserRepository
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize dependencies
user_repo = UserRepository()
user_service = UserService(user_repo)

@app.errorhandler(ValueError)
def handle_value_error(e):
    logger.warning(f"Validation error: {str(e)}")
    return jsonify({"error": str(e)}), 400

@app.errorhandler(Exception)
def handle_general_error(e):
    logger.error(f"Unexpected error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    user = user_service.create_user(
        data['username'], 
        data['email'], 
        data['password']
    )
    
    logger.info(f"User created: {user.username}")
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "is_active": user.is_active
    }), 201

@app.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password required"}), 400
    
    user = user_service.authenticate(data['username'], data['password'])
    
    if user:
        logger.info(f"User authenticated: {user.username}")
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })
    else:
        logger.warning(f"Failed authentication attempt for: {data['username']}")
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
        "is_active": user.is_active
    })

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "JSON body required"}), 400
    
    user = user_service.update_user(
        user_id,
        data.get('username'),
        data.get('email'),
        data.get('password')
    )
    
    logger.info(f"User updated: {user.username}")
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "updated_at": user.updated_at.isoformat(),
        "is_active": user.is_active
    })

@app.route('/users/<int:user_id>', methods=['DELETE'])
def deactivate_user(user_id):
    success = user_service.deactivate_user(user_id)
    
    if success:
        logger.info(f"User deactivated: {user_id}")
        return jsonify({"message": "User deactivated"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)