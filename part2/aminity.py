#!/usr/bin/python3


import uuid
from datetime import datetime
import re


class aminity:
    def __init__(self, id, name, description, available=True):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.available = available
        self.place = [] # List of places with this amenity

    # Check name validity
    def validity_name(name):
        # Length check (between 3 an 30 characters)
        if len(name) < 3 or len(name) > 30:
            return False
        
        # Character verification: letters, spaces, apostrophes and hyphens are allowed
        # Regex: ^ = start, $ = end, [a-zA-ZÀ-ÿ] = letters with accents
        # Apostrophes and hyphens are accepted between letters.
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", name):
            return False
        
        return True
    
    # Check validity description to the place
    def validity_description(description):
        # Length check (between 3 an 500 characters)
        if len(description) < 3 or len(description) > 500:
            return False
        
        # Character verification: letters, spaces, apostrophes and hyphens are allowed
        # Regex: ^ = start, $ = end, [a-zA-ZÀ-ÿ] = letters with accents
        # Apostrophes and hyphens are accepted between letters.
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", description):
            return False
        
        return True
    
    # Display the details of the aminity
    def __str__(self):
        return f"{self.name}: {self.description} (Available: {self.available})"

    # Define list of place
    def add_place(self, place):
        self.place.append(place)


    # Validity datetime
    def save(self):
        """Update the update_at timestamp whenever the object is modified"""
        self.created_at = datetime.now()
        self.update_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.item():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save() # Update the update_at timestamp