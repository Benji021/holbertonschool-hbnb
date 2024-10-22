#!/usr/bin/python3

import uuid
from datetime import datetime
import re


class review:
    def __init__(self, id, author, note, comment):
        self.id = str(uuid.uuid4())
        self.author = author
        self.note = note
        self.comment = comment
    
    # Generate the unique token
    def generer_token():
        return str(uuid.uuid4())
    
    # Check validity note
    def validity_note(note):
        if note < 0 or note > 5:
            raise ValueError("The score must be between 0 and 5.")
        return True
    
    # Check validity comment to the place
    def validity_comment(comment):
        # Length check (between 3 an 500 characters)
        if len(comment) < 3 or len(comment) > 500:
            return False
        
        # Character verification: letters, spaces, apostrophes and hyphens are allowed
        # Regex: ^ = start, $ = end, [a-zA-ZÀ-ÿ] = letters with accents
        # Apostrophes and hyphens are accepted between letters.
        if not re.match(r"^[a-zA-ZÀ-ÿ' -]+$", comment):
            return False
        
        return True
    
    # Display the details of the review.
    def display(self):
        print(f"author : {self.author}")
        print(f"note : {self.note}")
        print(f"comment : {self.comment}")


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