from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        if self.get_user_by_email(user_data['email']):
            raise ValueError('Email already registered')
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by their ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by their email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users from the repository."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information."""
        user = self.get_user(user_id)
        if not user:
            return None


        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError('Email already registered')

        try:
            user.update(user_data)
            return user
        except ValueError as e:
            raise ValueError(str(e))

    def create_place(self, place_data):
    # Logic to create a place, including validation for price, latitude, and longitude
        if not self._validate_place_data(place_data):
            return False

        new_place = {
            'name' : place_data.get('name'),
            'price' : place_data.get('price'),
            'latitude' : place_data.get('latitude'),
            'longitude' : place_data.get('longitude')
        }
        return self.place_repo.add(new_place)

    def _validate_place_data(self, place_data):
    # Logic to validate place data
        if not self._validate_price(place_data.get('price')):
            return False
        if not self._validate_coordinates(place_data.get('latitude'), place_data.get('longitude')):
            return False
        return True

    def _validate_price(self, price):
    # Logic to validate price data
        if not isinstance(price, (float, int)) or price < 0:
            raise ValueError("Price must be a positive number")
        return True

    def _validate_coordinates(self, latitude, longitude):
    # Logic to validate coordinates
        try:
            lat, lon = float(latitude), float(longitude)
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                raise ValueError("Coordinates out of range")
            return True
        except (TypeError, ValueError):
            raise ValueError("Please enter valid coordinates")

    def get_place(self, place_id):
    # Logic to retrieve a place by ID, including associated owner and amenities
        place = self.place_repo.get(place_id)
        if place:
            owner = self.user_repo.get(place.user_id)
            amenities = self.amenity_repo.get_by_place(place_id)
            place.owner = owner
            place.amenities = amenities
            return place
        return False

    def get_all_places(self):
    # Logic to retrieve all places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
    # Logic to update a place
        existing_place = self.place_repo.get(place_id)
        if not existing_place:
            raise ValueError("This place does not exist")

        if not self._validate_place_data(place_data):
            return False

        updated_place = {**existing_place, **place_data}
        return self.place_repo.update(place_id, updated_place)

    def create_review(self, review_data):
    # Logic to create a review, including validation for user_id, place_id, and rating
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')
        text = review_data.get('text')

        if not user_id or not place_id or not rating or not text:
            raise ValueError("Missing required fields: user_id, place_id, rating, or text")

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError('Rating must be an integer between 1 and 5')

        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)
        if not user:
            raise ValueError(f"User with ID {user_id} does not exists")
        if not place:
            raise ValueError(f"Place with ID {place_id} does not exist")

        new_review = {
            'user_id': user_id,
            'place_id': place_id,
            'rating': rating,
            'text': text
        }
        return self.review_repo.add(new_review)

    def get_review(self, review_id):
    # Logic to retrieve a review by ID
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} does not exist")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
    # Logic to retrieve all reviews for a specific place
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} does not exist")

        reviews = self.review_repo.get_all()
        return [review for review in reviews if review['place_id'] == place_id]

    def update_review(self, review_id, review_data):
    # Logic to update a review
        existing_review = self.review_repo.get(review_id)
        if not existing_review:
            raise ValueError(f"Review with ID {review_id} does not exist")

        if 'rating' in review_data:
            rating = review_data
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be an integer between 1 and 5")

        updated_review = {**existing_review, **review_data}

        return self.review_repo.update(review_id, updated_review)

    def delete_review(self, review_id):
    # Logic to delete a review
        existing_review = self.review_repo.get(review_id)
        if not existing_review:
            raise ValueError(f"Review with ID {review_id} does not exist")

        return self.review_repo.delete(review_id)

facade = HBnBFacade()
