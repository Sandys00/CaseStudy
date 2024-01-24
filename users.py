import os
from tinydb import TinyDB, Query
from serializer import serializer

class User:
    # Füge das db_connector Klassenattribut hinzu
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')

    def __init__(self, id, name) -> None:
        self.name = name
        self.id = id

    # Annahme: Diese Methode lädt einen Benutzer anhand seiner ID aus der Datenbank
    @classmethod
    def load_user_by_id(cls, user_id):
        # Check if the user with the given ID exists in the database
        result = cls.db_connector.search(Query().id == user_id)

        if result:
            # If found, create a User object and return it
            user_data = result[0]
            return cls(user_data['id'], user_data['name'])
        else:
            # If not found, return None
            return None
