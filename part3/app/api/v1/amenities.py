from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Operations related to amenities')
facade = HBnBFacade()

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
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
    def get(self):
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200 


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
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
    def put(self, amenity_id):
        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Invalid input data'}, 400

        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            return {'message': 'Amenity not found'}, 404

        return {'message': 'Amenity updated successfully'}, 200