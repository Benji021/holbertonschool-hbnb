#!/usr/bin/python3

import uuid
from datetime import datetime
import re


class user:
    def __init__(self, id, first_name, last_name, email, password):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    # Check first_name validity
    def validate_first_name(first_name):
        # Length check (between 3 an 30 characters)
        if len(first_name) < 3 or len(first_name) > 30:
            return False
        
        # Character verification: letters, spaces, apostrophes and hyphens are allowed
        # Regex: ^ = start, $ = end, [a-zA-ZÀ-ÿ] = letters with accents
        # Apostrophes and hyphens are accepted between letters.
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", first_name):
            return False
        
        return True

    # Check Last_name validity
    def validate_last_name(last_name):
        # Length check (between 3 an 30 characters)
        if len(last_name) < 3 or len(last_name) > 30:
            return False
        
        # Character verification: letters, spaces, apostrophes and hyphens are allowed
        # Regex: ^ = start, $ = end, [a-zA-ZÀ-ÿ] = letters with accents
        # Apostrophes and hyphens are accepted between letters.
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", last_name):
            return False
        
        return True
    
    # Check email validity
    def validate_email(email):
        if "@" and "." in email:
            return True
        else:
            return False
        
    # Check password validity
    def validate_password(password):
        # Check minimum password length
        if len(password) < 8:
            return "The password must be at least 8 characters long."
        
        # Check for capital letters
        if not re.search(r"[A-Z]", password):
            return "The password must contain at least one capital letter."
        
        # Check for lower-case letters
        if not re.search(r"[a-z]", password):
            return "The password must contain at least one lowercase letter."
        
        # Check the presence of a digit
        if not re.search(r"\d", password):
            return "The password must contain at least one digit."
        
        # Check for the presence of a special character
        if not re.search(r"[!@#$%^&*()_+=-]", password):
            return "The password must include at least one special character."
        
        return "The password is valid."

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