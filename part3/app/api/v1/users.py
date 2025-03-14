from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from flask import Blueprint, request, jsonify
from app.models import User

user_bp = Blueprint('user', __name__)

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=False, description='Admin status')
})

def admin_required(fn):
    """Décorateur pour restreindre l'accès aux administrateurs."""
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        current_user = facade.get_user_by_id(user_id)
        
        if not current_user or not current_user.is_admin:
            return jsonify({"error": "Accès refusé : Administrateur requis"}), 403
        
        return fn(*args, **kwargs)

    return wrapper
@api.route('/')
class UserList(Resource):
    @admin_required  # Only admins can create a user
    @api.expect(user_model, validate=True)  # Automatic field validation
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden: Admin access required')
    def post(self):
        """Create a new user (Admin only)"""
        user_data = api.payload

        email = user_data.get('email')
        if not email:
            return {'error': 'Email is required'}, 400
        
        # Check if the email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'List of users retrieved successfully')
    @jwt_required()  # Accessible to authenticated users
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_users()
        return [user.to_dict() for user in users], 200
    
    # Modèle pour l'input de mise à jour utilisateur
update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='New password of the user')
})
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()  # Accessible to authenticated users
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
    
    @api.expect(update_user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # Accessible to authenticated users
    def put(self, user_id):
        """Update a user's details (admin or user itself only)"""
        user_data = api.payload
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        if not current_user:
            return {'error': 'User not found'}, 404
        
        # Check if the target user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Check permissions: admin OR user itself
        if not current_user.is_admin and str(current_user_id) != str(user_id):
            return {'error': 'Forbidden: Not authorized to update this user'}, 403
        
        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400