from uuid import uuid4
from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity
from app.models.user import User
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def authenticate_user(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):  # Vérifie le mot de passe
            return user
        return None

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        user.update(**user_data)
        self.user_repo.update(user_id, user)
        return user

    def create_amenity(self, amenity_data):
        if not amenity_data or 'name' not in amenity_data:
            return None

        new_amenity = Amenity(amenity_data["name"])
        self.amenity_repo.add(new_amenity)

        print(f">>> Amenity created: {new_amenity.id}")

        return new_amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        print(f">>> Searching for Amenity ID {amenity_id}: Found? {amenity is not None}")
        return amenity

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [a.to_dict() for a in amenities]

    def update_amenity(self, amenity_id, data):
        print(f">>> Type de data reçu dans update(): {type(data)} - Contenu: {data}")

        if not isinstance(data, dict):
            raise TypeError(f"Expected 'data' to be a dict, got {type(data)} instead.")

        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        for key, value in data.items():
            setattr(amenity, key, value)

        if hasattr(self, "save"):
            self.save(amenity)
        
        return amenity

    def create_place(self, place_data):
    # Logic to create a place, including validation for price, latitude, and longitude
        if not self._validate_place_data(place_data):
            return {"error": "Invalid place data"}, 400
        
        owner_id = place_data.get('owner_id')
        if not owner_id:
            return {"error": "Owner is required"}, 400

        new_place = Place(
            id=str(uuid4()),
            owner_id=owner_id,
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude')
        )

        created_place = self.place_repo.add(new_place)

        return {
            "message": "Place successfully created",
            "place": {
                "id": created_place.id,
                "owner_id": created_place.owner_id,
                "title": created_place.title,
                "description": created_place.description,
                "price": created_place.price,
                "latitude": created_place.latitude,
                "longitude": created_place.longitude
            }
        }, 201

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