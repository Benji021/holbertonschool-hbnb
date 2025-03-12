from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import HBnBFacade
 
api = Namespace('amenities', description='Operations related to amenities')
admin_api = Namespace('admin_amenities', description='Admin operations related to amenities')
facade = HBnBFacade()
 
# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
     'name': fields.String(required=True, description='Name of the amenity')
 })
admin_amenity_model = admin_api.model('Amenity', {
     'name': fields.String(required=True, description='Name of the amenity')
 })
 
 
@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        data = api.payload
        if not data or 'name' not in data:
            return {'message': 'Invalid input data'}, 400
 
        amenity = facade.create_amenity(data)
        print(">>> Amenity returned from create_amenity:", amenity)
 
        if not amenity:
            return {'message': 'Failed to create amenity'}, 400
 
        return amenity.to_dict(), 201
 
    @api.response(200, 'List of amenities retrieved successfully')
    @jwt_required()
    def get(self):
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200 
 
 
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        print(f">>> Amenity fetched: {amenity}")
 
        if not amenity:
            return {'message': 'Amenity not found'}, 404
 
        return amenity.to_dict(), 200
 
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Invalid input data'}, 400
 
        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            return {'message': 'Amenity not found'}, 404
 
        return {'message': 'Amenity updated successfully'}, 200
 
 
@admin_api.route('/amenities')
class AdminAmenityCreate(Resource):
    @admin_api.expect(admin_amenity_model)
    @admin_api.response(201, 'Amenity successfully created')
    @admin_api.response(400, 'Invalid input data')
    @admin_api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'message': 'Admin privileges required'}, 403
         
        data = api.payload
        if not data or 'name' not in data:
            return {'message': 'Invalid input data'}, 400
        amenity = facade.create_amenity(data)

        if not amenity:
            return {'message': 'Failed to create amenity'}, 400

        return amenity.to_dict(), 201
 
@admin_api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @admin_api.expect(admin_amenity_model)
    @admin_api.response(200, 'Amenity updated successfully')
    @admin_api.response(404, 'Amenity not found')
    @admin_api.response(400, 'Invalid input data')
    @admin_api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'message': 'Admin privileges required'}, 403

        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Invalid input data'}, 400

        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            return {'message': 'Amenity not found'}, 404
        return {'message': 'Amenity updated successfully'}, 200