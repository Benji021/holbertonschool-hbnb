#!/usr/bin/python3

import uuid
from datetime import datetime

class review:
    def __init__(self, id, user, place, note, comment):
        self.id = str(uuid.uuid4())
        self.user = user
        self.place = place
        self.note = note
        self.comment = comment

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