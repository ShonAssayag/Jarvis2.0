from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,AutoReconnect
from pymongo.server_api import ServerApi


class MongodbConnection:
    def __init__(self, connection_uri: str, max_connections: int = 10):
        self.connection_uri = connection_uri
        self.max_connections = max_connections
        self.connection_pool = []
        self.current_connection = 0

    def get_connection(self):
        if self.current_connection >= self.max_connections:
            self.current_connection = 0
        if len(self.connection_pool) < self.max_connections:
            try:
                client = MongoClient(self.connection_uri, server_api=ServerApi('1'))
                self.connection_pool.append(client)
                self.current_connection += 1
                return client
            except ConnectionFailure as e:
                raise Exception("Failed to connect to MongoDB server:", e)
        else:
            self.current_connection += 1
            return self.connection_pool[self.current_connection - 1]

    def close_all_connections(self):
        for connection in self.connection_pool:
            connection.close()

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

