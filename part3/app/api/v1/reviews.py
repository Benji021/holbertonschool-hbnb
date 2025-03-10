from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required() # Requires a JWT token to access this route
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        if not api.payload:
            return {'error': 'Request payload is missing or invalid'}, 400
        
        current_user = get_jwt_identity()  # Recover logged-in user ID
        review_data = api.payload
        place_id = review_data.get("place_id")

        # Check that the location exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': "Place not found"}, 404
        
        # Prevent an owner from rating his own location
        if place["owner_id"] == current_user:
            return {'error': "You cannot review your own place"}, 403
        
        # Check if the user has already left a review for this location
        existing_review = facade.get_review_by_user_and_place(current_user, place_id)
        if existing_review:
            return {'error': "You have already reviewed this place"}, 403
        
        try:
            review_data = api.payload
            new_review = facade.create_review(review_data)
            return {'message': 'Review successfully created', 'review': new_review}, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
            return {'reviews': reviews}, 200
        except Exception as e:
            return {'error': f'An unexpected error occurred: {str(e)}'}, 500

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            return {'review': review}, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @jwt_required() # Requires a JWT token to access this route
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        if not api.payload:
            return {'error': "Request payload is missing or invalid"}, 400
        
        current_user = get_jwt_identity() # Recover logged-in user ID

        # Check that review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': "Review not found"}, 404

        # Check if the user is the author of the review
        if review["user_id"] != current_user:
            return {'error': "You are not authorized to update this review"}, 403

        try:
            updated_data = api.payload
            updated_review = facade.update_review(review_id, updated_data)
            return {'message': 'Review successfully updated', 'review': updated_review}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required() # Requires a JWT token to access this route
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()  # Recover logged-in user ID

        # Check that review exists
        review = facade.get_review(review_id)
        if not review:
            return {'error': "Review not found"}, 404

        # Check if the user is the author of the review
        if review["user_id"] != current_user:
            return {'error': "You are not authorized to delete this review"}, 403
                    
        try:
            facade.delete_review(review_id)
            return {'message': "Review successfully deleted"}, 200
        except ValueError as e:
            return {'error': str(e)}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            if not facade.get_place(place_id):
                raise ValueError(f"Place with ID {place_id} does not exist")

            reviews = facade.get_reviews_by_place(place_id)
            return {'reviews': reviews}, 200
        except ValueError as e:
            return{'error': str(e)}, 404