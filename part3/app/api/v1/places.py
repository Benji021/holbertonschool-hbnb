from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        owner = place_data.get('owner_id', None)

        if owner is None or len(owner) == 0:
            return {'error': 'Invalid input data.'}, 400

        user = facade.user_repo.get_by_attribute('id', owner)
        if not user:
            return {'error': 'Invalid input data'}, 400
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
        return place.to_dict_list(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        try:
            facade.update_place(place_id, place_data)
            return {'message': 'Place updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenities added successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def post(self, place_id):
        amenities_data = api.payload
        if not amenities_data or len(amenities_data) == 0:
            return {'error': 'Invalid input data'}, 400
        
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        for amenity in amenities_data:
            a = facade.get_amenity(amenity['id'])
            if not a:
                return {'error': 'Invalid input data'}, 400
        
        for amenity in amenities_data:
            place.add_amenity(amenity)
        return {'message': 'Amenities added successfully'}, 200

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
    
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def get(self, place_id):
        """Get place details by ID"""
        current_user = get_jwt_identity()
        try:
            place = facade.get_place(place_id)
            if place["owner_id"] != current_user["id"]:
                return {'error': 'Unauthorized action'}, 403
            return place
        except ValueError as e:
            return {'error': str(e)}, 404
 
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Admin or owner can update a place"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place['owner_id'] != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        try:
            updated_place = facade.update_place(place_id, api.payload)
            return {'message': 'Place successfully updated', 'place': updated_place}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @admin_api.response(200, 'Place deleted successfully')
    @admin_api.response(404, 'Place not found')
    @admin_api.response(403, 'Unauthorized action')
    def delete(self, place_id):
        """Admin or owner can delete a place"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place['owner_id'] != current_user['id']:
            return {'error': 'Unauthorized action'}, 403
        if facade.delete_place(place_id):
            return {'message': 'Place deleted successfully'}, 200
        return {'error': 'Place not found'}, 404
 
@admin_api.route('/<place_id>')
class AdminPlaceModify(Resource):
    @admin_api.expect(place_model)
    @admin_api.response(200, 'Place updated successfully')
    @admin_api.response(404, 'Place not found')
    @admin_api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()
        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
 
        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        if not api.payload:
            return {'message': 'Request payload is missing or invalid'}, 400
        try:
            updated_data = api.payload
            updated_place = facade.update_place(place_id, updated_data)
            return {'message': 'Place successfully updated', 'place': updated_place}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
 
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')
        place = facade.get_place(place_id)
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
 
        deleted = facade.delete_place(place_id)
        if not deleted:
            return {'error': 'Place not found'}, 404
 
        return {'message': 'Place deleted successfully'}, 200
    @api.marshal_with(place_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
       """Get place details by ID"""
       try:
           place = facade.get_place(place_id)
           return place
       except ValueError as e:
           return {'error': str(e)}, 404

    @jwt_required()  # Requires authentication to modify a location
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
       """Update a place's information"""
       if not api.payload:
           return {'message': 'Request payload is missing or invalid'}, 400
        
       current_user = get_jwt_identity()  # Recover logged-in user ID

       # Retrieve location details to verify owner
       place = facade.get_place(place_id)
       if not place:
           return {'error': 'Place not found'}, 404
        
       # Check that the authenticated user is the owner of the site
       if place['owner_id'] != current_user:
           return {'error': "You are not authorized to update this place"}, 403
        
       try:
           updated_data = api.payload
           updated_place = facade.update_place(place_id, updated_data)
           return {'message': 'Place successfully updated', 'place': updated_place}, 200
       except ValueError as e:
           return {'error': str(e)}, 400
    @api.marshal_with(place_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
       """Get place details by ID"""
       try:
           place = facade.get_place(place_id)
           return place
       except ValueError as e:
           return {'error': str(e)}, 404

    @jwt_required()  # Requires authentication to modify a location
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
       """Update a place's information"""
       if not api.payload:
           return {'message': 'Request payload is missing or invalid'}, 400
       
       current_user = get_jwt_identity()  # Recover logged-in user ID

       # Retrieve location details to verify owner
       place = facade.get_place(place_id)
       if not place:
           return {'error': 'Place not found'}, 404
        
       # Check that the authenticated user is the owner of the site
       if place['owner_id'] != current_user:
           return {'error': "You are not authorized to update this place"}, 403
        
       try:
           updated_data = api.payload
           updated_place = facade.update_place(place_id, updated_data)
           return {'message': 'Place successfully updated', 'place': updated_place}, 200
       except ValueError as e:
           return {'error': str(e)}, 400