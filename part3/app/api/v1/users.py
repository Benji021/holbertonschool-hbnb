from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade
 
api = Namespace('users', description='User operations')
admin_api = Namespace('admin', description='Admin operations')
 
# Define the user model for input validation and documentation
user_model = api.model('User', {
@@ -17,6 +19,7 @@ class UserList(Resource):
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new user"""
        user_data = api.payload
@@ -51,6 +54,7 @@ def get(self, user_id):
    @api.expect(user_model, validate=True)  # Ajoute la validation
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user details"""
        user = facade.get_user(user_id)
@@ -68,4 +72,67 @@ def put(self, user_id):
                'last_name': user.last_name,
                'email': user.email
             }
        }, 200
 
@admin_api.route('/users')
class AdminUserCreate(Resource):
    @admin_api.expect(user_model, validate=True) # Ajoute la validation
    @admin_api.response(201, 'User successfully created')
    @admin_api.response(400, 'Email already registered')
    @admin_api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
         
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
         
        new_user = facade.create_user(user_data)
        return {'id': new_user.id, 'message': 'User created sucessfuly'}, 201
 
@admin_api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @admin_api.expect(user_model, validate=True)  # Ajoute la validation
    @admin_api.response(200, 'User successfully updated')
    @admin_api.response(404, 'User not found')
    @admin_api.response(400, 'Email already registered')
    @admin_api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
     
        user_data = api.payload
 
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
     
        new_email = user_data.get('email')
        if new_email and new_email != user.email:
            existing_user = facade.get_user_by_email(new_email)
            if existing_user:
                return {'error': 'Email already registered'}, 400
 
        updated_fields = {}
        if new_email:
            updated_fields['email'] = new_email
        if 'password' in user_data:
            user.hash_password(user_data['password'])
            updated_fields['password'] = user.password
         
        updated_user = facade.update_user(user_id, **updated_fields)
         
        return {
            'message': 'User successfuly updated',
            'user': {
                'id': updated_user.id,
                'email': updated_user.email
            }
         }, 200