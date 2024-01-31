import os
from users import User
from datetime import datetime
from tinydb import TinyDB, Query
from serializer import serializer
from tinydb_serialization import SerializationMiddleware   
from tiny_db_with_class_attributes import reservation
import streamlit as st



class Device():
    # Class variable that is shared between all instances of the class
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')

    # Constructor
    def __init__(self, device_name : str, managed_by_user_id: str, end_of_life: datetime, first_maintenance: datetime, next_maintenance: datetime,
                 maintenance_interval: int, maintenance_cost: float, reservation_start: datetime = None, reservation_end: datetime = None):
        self.device_name = device_name
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True
        self.end_of_life = end_of_life
        self.first_maintenance = first_maintenance
        self.next_maintenance = next_maintenance
        self.__maintenance_interval = maintenance_interval
        self.__maintenance_cost = maintenance_cost
        self.reservation_start = reservation_start
        self.reservation_end = reservation_end
        
    # String representation of the class
    def __str__(self):
        return f'Device {self.device_name} ({self.managed_by_user_id})'

    # String representation of the class
    def __repr__(self):
        return self.__str__()
    
    # speichere die Daten in der Datenbank
    def store_data(self):
        # Check if the device already exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)

        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(
                {
                    "device_name": self.device_name,
                    "managed_by_user_id": self.managed_by_user_id,
                    "is_active": self.is_active,
                    "end_of_life": self.end_of_life,
                    "first_maintenance": self.first_maintenance,
                    "next_maintenance": self.next_maintenance,
                    "_Device__maintenance_interval": self._Device__maintenance_interval,
                    "_Device__maintenance_cost": self._Device__maintenance_cost,
                    "reservation_start": self.reservation_start,
                    "reservation_end" : self.reservation_end
                },
                doc_ids=[result[0].doc_id],
            )
            st.success(f"Daten für Gerät {self.device_name} erfolgreich aktualisiert.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            st.success(f"Daten für Gerät {self.device_name} erfolgreich eingefügt.")

            
    # Class method that can be called without an instance of the class to construct an instance of the class
    @classmethod
    def load_all_devices(cls):
        # Lade alle Geräte aus der Datenbank
        result = cls.db_connector.all()
        if result:
            data = result[0]
            return data
        else:
            return None
        
    @classmethod
    def get_all_names(cls):
        result = cls.db_connector.all()
        if result:
            device_names = [data["device_name"] for data in result]
            return device_names
        else:
            return None
    
    @classmethod
    def get_all_names_for_reservation(cls):
        result = cls.db_connector.all()
        if result:
            device_names = [data["device_name"] for data in result if data["reservation_start"] == None]
            return device_names
        else:
            return None
        
    @classmethod
    def get_all_names_for_change_reservation(cls):
        result = cls.db_connector.all()
        if result:
            device_names = [data["device_name"] for data in result if data["reservation_start"] != None]
            return device_names
        else:
            return None
    
    @classmethod
    def load_device_by_name(cls, device_name):
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery.device_name == device_name)
        if result:
            data = result[0]
            return data
        else:
            return None

        
    
    

class reservation():
    def __init__(self, name:str, start_date:datetime, end_date:datetime):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def to_dict(self):
        return self.__dict__


if __name__ == "__main__":
    # Create a device
    device1 = Device("Device1", "one@mci.edu")
    device2 = Device("Device2", "two@mci.edu") 
    device3 = Device("Device3", "two@mci.edu") 
    device1.store_data()
    device2.store_data()
    device3.store_data()
    device4 = Device("Device3", "four@mci.edu") 
    device4.store_data()

    loaded_device = Device.load_data_by_device_name('Device2')
    if loaded_device:
        print(f"Loaded Device: {loaded_device}")
    else:
        print("Device not found.")
    