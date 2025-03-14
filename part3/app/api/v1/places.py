from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from flask import jsonify
from app.services import facade

def admin_or_owner_required(fn):
    """Decorator to allow admins or owners of a place to modify/delete it"""
    @wraps(fn)
    @jwt_required()
    def wrapper(place_id, *args, **kwargs):
        user_id = get_jwt_identity()
        current_user = facade.get_user_by_id(user_id)

        if not current_user:
            return jsonify({"error": "User not found"}), 404
        
        place = facade.get_place(place_id)
        if not place:
            return jsonify({"error": "Place not found"}), 404
        
        # Check if the user is admin or owner of the place
        if not current_user.is_admin and place.owner_id != user_id:
            return jsonify({"error": "Forbidden: You do not have permission"}), 403

        return fn(place_id, *args, **kwargs)

    return wrapper

api = Namespace('places', description='Place operations')

# Models
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details')
})

amenities_list_model = api.model('AmenitiesList', {
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# Routes
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        owner = place_data.get('owner_id')

        if not owner:
            return {'error': 'Invalid input data: owner_id is required'}, 400

        user = facade.user_repo.get_by_attribute('id', owner)
        if not user:
            return {'error': 'Invalid input data: owner does not exist'}, 400
        
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @admin_or_owner_required
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        try:
            updated_place = facade.update_place(place_id, place_data)
            return {'message': 'Place updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Forbidden')
    @admin_or_owner_required
    def delete(self, place_id):
        """Delete a location (admin or owner only)"""
        try:
            facade.delete_place(place_id)
            return {"message": "Place deleted successfully"}, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect(amenities_list_model)
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        """Add amenities to a place"""
        amenities_data = api.payload.get('amenities', [])
        if not amenities_data:
            return {'error': 'Invalid input data: amenities list is required'}, 400
        
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        for amenity_id in amenities_data:
            if not facade.get_amenity(amenity_id):
                return {'error': f'Amenity with ID {amenity_id} not found'}, 400
        
        try:
            facade.add_amenities_to_place(place_id, amenities_data)
            return {'message': 'Amenities added successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in place.reviews], 200
