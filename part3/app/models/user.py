#!/usr/bin/python3
""" Defining the user class, its attributes and relationships """
import re
import uuid
from datetime import datetime
from app.models.place import Place
from app.models.review import Review
from app import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

class User():
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__() # Initialize parent class

        # Generate a unique ID
        self.id = str(uuid.uuid4())

        # Field checks
        self.first_name = self.validate_name(first_name, "first name")
        self.last_name = self.validate_name(last_name, "last name")
        self.email = self.validate_email(email)
        self.hash_password(password)
        self.is_admin = is_admin

        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        #Relation
        self.place = [] # List of places owned by the user
        self.reviews = [] # List of reviews written by the user

    def add_place(self, place):
        """ Associate a location with this user """
        if isinstance(place, Place):
            self.place.append(place)
            place.owner = self # Set user as owner
        else:
            raise TypeError("The object added must be an instance of Place")

    def add_review(self, review):
        """ Associate a notice with this user """
        if isinstance(review, Review):
            self.reviews.append(review)
            review.user = self # Define user as review author
        else:
            raise TypeError("The object added must be a Review instance")

    @staticmethod
    def validate_name(name, field_name):
        """ Checks that the name is a string of max 50 characters. """
        if not isinstance(name, str) or len(name) > 50:
            raise ValueError(f"{field_name} must be a string of max 50 characters.")
        return name.strip()

    @staticmethod
    def validate_email(email):
        """ Checks that the email is valid. """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            raise ValueError("Invalid e-mail address.")
        return email.strip().lower()

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def update(self, first_name=None, last_name=None, email=None, is_admin=None):
        """ Updates user information. """
        if first_name:
            self.first_name = self.validate_name(first_name, "first name")
        if last_name:
            self.last_name = self.validate_name(last_name, "last name")
        if email:
            self.email = self.validate_email(email)
        if is_admin is not None:
            self.is_admin = is_admin

        self.updated_at = datetime.now()


    def show_info(self):
        """ Displays user information. """
        return (f"ID: {self.id}\n"
                f"Name: {self.first_name} {self.last_name}\n"
                f"Email: {self.email}\n"
                f"Admin: {'Yes' if self.is_admin else 'No'}\n"
                f"Created_at: {self.created_at}\n"
                f"Update_at: {self.update_at}")