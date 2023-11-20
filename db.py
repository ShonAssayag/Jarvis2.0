from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,AutoReconnect
from pymongo.server_api import ServerApi


class MongodbConnection:
    def __init__(self, connection_uri: str):
        self.connection_uri = connection_uri

    def get_connection(self):
        try:
            client = MongoClient(self.connection_uri, server_api=ServerApi('1'))
            return client
        except ConnectionFailure as e:
            raise Exception("Failed to connect to MongoDB server:", e)

    def get_database(self, database_name):
        client = self.get_connection()
        db = client[database_name]
        return db

    def get_collection(self, database_name, collection_name):
        db = self.get_database(database_name)
        collection = db[collection_name]
        return collection

    def handle_exceptions(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ConnectionFailure as e:
                raise Exception(f"Failed to connect to MongoDB: {e}")
            except Exception as e:
                raise Exception(f"Unexpected error: {e}")

        return wrapper

