from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

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
