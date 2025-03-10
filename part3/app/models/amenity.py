#!/usr/bin/python3
""" Defining the aminity class, its attributes and relationships """


import uuid
from datetime import datetime

class Amenity:
    def __init__(self, name: str):
        if len(name) > 50:
            raise ValueError("Equipment name must not exceed 50 characters")

        # Generate a unique ID
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def update(self, new_data):
        """ Update equipment name """
        print(f">>> Type de new_data: {type(new_data)}, Contenu: {new_data}")

        if not isinstance(new_data, dict):
            raise TypeError(f"Expected 'new_data' to be a dict, got {type(new_data)}")
        
        for key, value in new_data.items():
            setattr(self, key, value)

        new_name = new_data.get("name")
    
        print(f">>> Extracted new_name: {new_name}")
        
        if not isinstance(new_name, str):
            raise TypeError(f"Expected a string for 'name', got {type(new_name)}")
        
        if len(new_name) > 50:
            raise ValueError("Equipment name must not exceed 50 characters")

        self.name = new_name
        self.updated_at = datetime.now()

    def to_dict(self):
        """ Convert the object into a JSON serializable dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __str__(self):
        return f"Amenity(id={self.id}, name={self.name}, created_at={self.created_at}, updated_at={self.updated_at})"