import os
from tinydb import TinyDB, Query

class User:

    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('users')

    # Constructor
    def __init__(self, id, user_name) -> None:
        self.user_name = user_name
        self.id = id

    def __str__(self) -> str:
        return f'User {self.id} ({self.user_name})'
    
    # Saves data in the database
    def store_data(self):
        print("Storing user data...")
        # Check if the User already exists in the database
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.user_name == self.user_name)
        if result:
# Update the existing record with the current instance's data
            #?result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("User existiert bereits.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert({'name':self.user_name, 'id':self.id})
            print("User data inserted.")


    # Class method that can be called without an instance of the class to
    # construct an instance of the class

    @classmethod
    def see_if_user_exists(cls, user_name):

        print('Daten werden überprüft.')
        UserQuery = Query()                                   
        result = cls.db_connector.search(UserQuery.user_name == user_name)

        if result:
            print('Dieser Benutzername existiert bereits.')
            return True
        else:
         return False