import os
from tinydb import TinyDB, Query
def find_devices() -> list:
    """Find all devices in the database."""
    # Define the database connector
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('devices')
    # Create a query object
    DeviceQuery = Query()
    # Search the database for all devices that are active
    result = db_connector.all()
    # The result is a list of dictionaries, we only want the device names
    if result:
        result = [x["device_name"] for x in result]
    return result