#!/usr/bin/python3

import uuid
from datetime import datetime
import re


class place:
    def __init__(self, id, name, address, city, country, description, price, location):
        self.id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.city = city
        self.country = country
        self.description = description
        self.price = None
        self.set_price(price)
        self.location = location
        self.user = None

    # Generate the unique token
    def generer_token():
        return str(uuid.uuid4())
    
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
    
    # Check validity address
    def validity_address(address):
        # Length check (between 3 an 50 characters)
        if len(address) < 3 or len(address) > 50:
            return False
        
        # Character verification: letters, spaces, apostrophes and hyphens are allowed
        # Regex: ^ = start, $ = end, [a-zA-ZÀ-ÿ] = letters with accents
        # Apostrophes and hyphens are accepted between letters.
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", address):
            return False
        
        return True
    
    # Check validity city
    def validity_city(city):
        # Length check (between 3 an 20 characters)
        if len(city) < 3 or len(city) > 20:
            return False
        
        # Character verification: letters, spaces, apostrophes and hyphens are allowed
        # Regex: ^ = start, $ = end, [a-zA-ZÀ-ÿ] = letters with accents
        # Apostrophes and hyphens are accepted between letters.
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", city):
            return False
        
        return True
    
    # Check validity country
    def validity_country(country):
        # Length check (between 3 an 20 characters)
        if len(country) < 3 or len(country) > 20:
            return False
        
        # Character verification: letters, spaces, apostrophes and hyphens are allowed
        # Regex: ^ = start, $ = end, [a-zA-ZÀ-ÿ] = letters with accents
        # Apostrophes and hyphens are accepted between letters.
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", country):
            return False
        
        return True
    
    # Returns the full address of the location
    def get_full_address(self):
        return f"{self.name}, {self.address}, {self.city}, {self.country}"
    
    # Check validity description
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

    # Return the full description of the location
    def get_full_description(self):
        return f"{self.description}"
    
    # Obtain the price
    def get_price(self):
        return self.price
    
    # Check validity and modify the price of the location
    def set_price(self, new_price):
        # Type of validity 
        if not isinstance(new_price, (int, float)):
            raise TypeError("The price must be a number (integer or floating).")
        
        # Positive validity of price
        if new_price < 0:
            raise ValueError("The price cannot be negative.")
        
        self.price = new_price

    # Return the price of the location
    def get_full_price(self):
        return f"{self.price}"


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