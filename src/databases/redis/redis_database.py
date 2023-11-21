from src.utils.init_db_conn import jarvis_db as db, cluster_connection
from src.utils.init_db_conn import get_transaction_connection

collection = db.get_collection('redis_databases')


@cluster_connection.handle_exceptions
def add_database(database: dict):
    transaction_connection = get_transaction_connection()

    def callback(session):
        clusters_collection = session.client.Jarvis.redis_clusters
        database_collection = session.client.Jarvis.redis_databases
        cluster_result = clusters_collection.find_one_and_update(
            {"name": {"$in": database['participating_clusters']}},
            {
                "$push": {"databases": database['name']},
                "$inc": {"allocated_memory": database['max_memory']}
            },
            session=session,
        )
        if cluster_result:
            database_result = database_collection.insert_one(database, session=session)
        else:
            return None

        return [cluster_result, database_result]

    with transaction_connection.start_session() as s:
        return s.with_transaction(callback)


@cluster_connection.handle_exceptions
def delete_database_by_name(cluster_name: str, database_name: str):
    transaction_connection = get_transaction_connection()

    def callback(session):
        clusters_collection = session.client.Jarvis.redis_clusters
        database_collection = session.client.Jarvis.redis_databases
        database_max_memory = float(database_collection.find_one({"name": database_name}, {"_id": 0, "max_memory": 1})['max_memory'])
        cluster_result = clusters_collection.find_one_and_update(
            {"name": cluster_name},
            {
                "$pull": {"databases": database_name},
                "$inc": {"allocated_memory": -database_max_memory}
            },
            session=session,
        )
        if cluster_result:
            database_result = database_collection.find_one_and_delete({"name": database_name}, session=session)
            return database_result
        else:
            return None

    with transaction_connection.start_session() as s:
        return s.with_transaction(callback)


@cluster_connection.handle_exceptions
def get_database_by_name(cluster_name: str, database_name: str):
    database = collection.find_one(filter={"participating_clusters": {"$in": [cluster_name]}, "name": database_name})
    if database:
        return database
    return None


@cluster_connection.handle_exceptions
def get_database_by_alias(alias_name: str):
    dot_split = alias_name.split(".")
    port = int(dot_split[0].split("-")[1])
    cluster_name = dot_split[1]
    database = collection.find_one(filter={"participating_clusters": {"$in": [cluster_name]}, "port": port})
    if database:
        return database
    return None
