from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade
from flask_jwt_extended import jwt_required, get_jwt_identity
 
api = Namespace('reviews', description='Review operations')
admin_api = Namespace('admin_reviews', description='Admin review operations')
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
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        if not api.payload:
            return {'message': 'Request payload is missing or invalid'}, 400
        try:
            review_data = api.payload
            if not facade.get_place(review_data['place_id']):
                return {'messsage': 'Place does not exist'}, 404
            if review_data['user_id'] != current_user['id']:
                return {'messsage': 'User ID does not match current user'}, 403
            new_review = facade.create_review(review_data)
            return {'message': 'Review successfully created', 'review': new_review}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
 
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
            return {'reviews': reviews}, 200
        except Exception as e:
            return {'message': f'An unexpected message occurred: {str(e)}'}, 500
 
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
            return {'message': str(e)}, 404
 
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        if not api.payload:
            return {'message': "Request payload is missing or invalid"}, 400
        try:
            updated_data = api.payload
            updated_review = facade.update_review(review_id, updated_data)
            return {'message': 'Review successfully updated', 'review': updated_review}, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
            return {'message': "Review successfully deleted"}, 200
        except ValueError as e:
            return {'message': str(e)}, 404

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
            return{'message': str(e)}, 404

@admin_api.route('/reviews/<review_id>')
class AdminReviewModify():
    @admin_api.response(200, 'Review deleted succesfuly')
    @admin_api.response(404, 'Review not found')
    @admin_api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        if not is_admin:
            return {'message': 'Unauthorized action'}, 403
        
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'message': 'Review not found'}, 404
        return {'message': 'Review deleted successfuly'}, 200