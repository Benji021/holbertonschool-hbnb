from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade


api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

def admin_required(fn):
    """Decorator to restrict access to administrators."""
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        current_user = facade.get_user_by_id(user_id)

        if not current_user or not current_user.is_admin:
            return {'error': 'Access denied: Administrator required'}, 403

        return fn(*args, **kwargs)

    return wrapper
@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Amenity already exists')
    @api.response(400, 'Invalid input data')
    @admin_required  # Restrict access to admins
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        
        existing_amenity = facade.amenity_repo.get_by_attribute('name', amenity_data.get('name'))
        if existing_amenity:
            return {'error': 'Invalid input data'}, 400
        
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @admin_required  # Only an admin can modify a convenience
    def put(self, amenity_id):
        amenity_data = api.payload

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        # Check if the name is empty or missing
        new_name = amenity_data.get('name', '').strip()
        if not new_name:
            return {'error': 'Invalid input data: name is required'}, 400

        # Check if the name is already in use by another commodity
        existing_amenity = facade.amenity_repo.get_by_attribute('name', new_name)
        if existing_amenity and existing_amenity.id != amenity.id:
            return {'error': 'Amenity with this name already exists'}, 400
        
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return updated_amenity.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400