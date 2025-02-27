from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity
from app.models.user import User


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

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
        return {"id": new_amenity.id, "name": new_amenity.name}

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [{"id": a.id, "name": a.name} for a in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity or 'name' not in amenity_data:
            return None

        amenity.update(amenity_data["name"])
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

facade = HBnBFacade()