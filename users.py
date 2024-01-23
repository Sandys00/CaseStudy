import os
from tinydb import TinyDB, Query

class User:

    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('users')

    # Constructor
    def __init__(self, id, user_name) -> None:
        self.user_name = user_name
        self.id = id

    # Den folgenden Code benötigt man hier und bei den Devices
         
    def store_data(self):
        print("Storing user data...")
        # Check if the device already exists in the database
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.user_name == self.user_name)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("User data updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("User data inserted.")
    # Class method that can be called without an instance of the class to
    # construct an instance of the class


    @classmethod
    def load_data_by_user_name(cls, user_name):
        # Load data from the database and create an instance of the Device class
        UserQuery = Query()                                   
        result = cls.db_connector.search(UserQuery.user_name == user_name)
        if result:
            data = result[0]
            return cls(data['id'], data['name'])
        else:
         return None