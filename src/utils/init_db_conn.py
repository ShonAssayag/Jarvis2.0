import os
from db import MongodbConnection

cluster_connection = MongodbConnection(os.environ.get("JARVIS_CONNECTION_STRING"))
connection = cluster_connection.get_connection()
jarvis_db = cluster_connection.get_database(os.environ.get("DB_NAME"))
