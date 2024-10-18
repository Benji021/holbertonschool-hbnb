#!/usr/bin/python3

import uuid
from datetime import datetime

class place:
    def __init__(self, id, name, description, location, price):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.location = location
        self.price = price

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