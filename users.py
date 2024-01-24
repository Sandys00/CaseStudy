import os
from tinydb import TinyDB
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
        # Implementiere hier die Logik zum Laden des Benutzers aus der Datenbank
        # Verwende eine Datenbankabfrage, um den Benutzer anhand seiner ID zu finden
        # Rückgabe könnte ein Benutzerobjekt sein oder None, wenn der Benutzer nicht gefunden wurde
        pass
