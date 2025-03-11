from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade

api = Namespace('places', description='Place operations')
facade = HBnBFacade()

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

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required() # Requires a JWT token to access this route
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        if not api.payload:
            return {'error': 'Request payload is missing or invalid'}, 400
        
        current_user = get_jwt_identity()  # Recover logged-in user ID
        place_data = api.payload

        # Check that the logged-in user is the owner of the location
        if place_data.owner_id != current_user:
            return {'error': "You can only create places under your own account"}, 403

        try:
            place_data = api.payload
            created_place = facade.create_place(place_data)
            if created_place:
                return {'message': 'Place successfully created', 'place': created_place}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.marshal_with(place_model, as_list=True)
    @api.response(200, description='List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            return places
        except Exception as e:
            return {'error': f'An unexpected error occurred: {str(e)}'}, 500

@api.route('/<place_id>')
class PlaceResource(Resource):
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