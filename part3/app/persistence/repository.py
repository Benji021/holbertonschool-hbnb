from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._data = {}

    def save(self, amenity):
        """Saves an updated amenity in memory storage"""
        self.data[amenity.id] = amenity  # Simulates backup

    def add(self, obj):
        self._data[obj.id] = obj

    def get(self, obj_id):
        return self._data.get(obj_id)

    def get_all(self):
        return list(self._data.values())

    def update(self, amenity_id, data):
        print(f">>> Type de data reçu dans update(): {type(data)} - Contenu: {data}")

        if not isinstance(data, dict):
            raise TypeError(f"Expected 'data' to be a dict, got {type(data)} instead.")
    
        amenity = self.get(amenity_id)
        if not amenity:
            return None

        for key, value in data.items():
            setattr(amenity, key, value)

        if hasattr(self, "save"):
            self.save(amenity)

        return amenity

    def delete(self, obj_id):
        if obj_id in self._data:
            del self._data[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._data.values() if getattr(obj, attr_name) == attr_value), None)