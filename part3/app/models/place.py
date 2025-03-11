#!/usr/bin/python3
""" Defining the place class, its attributes and relationships """


import uuid
from datetime import datetime
from app.models.review import Review
from app.models.user import User

class Place:
    def __init__(self, id,  title, price, latitude, longitude, owner_id, description=None):
        """ Initialization of a location with input validation """
        super().__init__() # Initialize parent class

        # Generate a unique ID
        self.id = str(uuid.uuid4())

        # Field Check
        self.title = self.validate_title(title)
        self.description = description if description else ""
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner_id)
        self.created_at = datetime.now()
        self.updated_at = self.created_at
 
        self.owner = self.get_user(owner_id)  # Retrieves the user with this ID
        if not self.owner:
            raise ValueError(f"Invalid owner_id: No user found with ID {owner_id}")

        # Relation
        self.amenities = [] # Equipment list
        self.reviews = [] # List of reviews associated with this location

        self.owner.add_place(self)

    def get_user(self, owner_id):
        """ Convertit owner_id en un objet User si c'est un ID """
        if isinstance(owner_id, User):  # If it's already a User, we keep it
            return owner_id
        elif isinstance(owner_id, str): # If it's an ID, we look for the User object
            return self.find_user_by_id(owner_id)
        return None

    @staticmethod
    def find_user_by_id(user_id):
        """ Simule la récupération d'un utilisateur par son ID (à remplacer par une requête DB) """
        # Fictitious example (replace this part with your ORM query)
        users_db = {
            "1234": User("Alice", "Dupont", "alice@example.com"),
            "5678": User("Bob", "Martin", "bob@example.com")
        }
        return users_db.get(user_id, None)  # Returns None if ID does not exist

    def get_owner_object(self, owner_id):
        """ Retrieves the User object associated with owner_id """
        user = User.get(owner_id)  # Recover user ID
        if not user:
            raise ValueError(f"Aucun utilisateur trouvé avec l'ID {owner_id}")
        return user

    def add_aminity(self, aminity):
        """ Associate a piece of equipment with this location """
        if isinstance(aminity, aminity):
            self.amenities.append(aminity)
        else:
            raise TypeError("The object added must be an instance of Amenity")

    def add_review(self, review):
        """ Associates a notice with this location """
        if isinstance(review, Review):
            self.reviews.append(review)
            review.place = self # Associate notice with this location
        else:
            raise TypeError("The object added must be an instance of Review")

    def validate_title(self, title):
        """ Validate Title """
        if not title or len(title) > 100:
            raise ValueError("The title is mandatory and must not exceed 100 characters.")
        return title

    def validate_price(self, price):
        """ Validate Price """
        if price < 0:
            raise ValueError("The price must be a positive value.")
        return price

    def validate_latitude(self, latitude):
        """ Validate Latitude """
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        return latitude

    def validate_longitude(self, longitude):
        """ Validate Longitude """
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        return longitude

    def validate_owner(self, owner):
        """ Validates the owner's existence """
        if not owner:
            raise ValueError("A valid owner is required.")
        return owner

    def update(self, **kwargs):
        """ Updates location attributes and timestamp """
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id" and key != "created_at":
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def __str__(self):
        return f"{self.title} - {self.price}€/night, {self.latitude}, {self.longitude} (Owner: {self.owner})"
    