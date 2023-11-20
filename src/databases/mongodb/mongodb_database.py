from fastapi import HTTPException

from src.utils.init_db_conn import jarvis_db as db, cluster_connection
from src.utils.init_db_conn import get_transaction_connection

collection = db.get_collection('mongodb_databases')


@cluster_connection.handle_exceptions
def add_database(cluster_name: str, database: dict):
    transaction_connection = get_transaction_connection()

    def callback(session):
        clusters_collection = session.client.Jarvis.mongodb_clusters

        database_collection = session.client.Jarvis.mongodb_databases

        cluster_result = clusters_collection.find_one_and_update(
            {"name": cluster_name},
            {
                "$push": {"databases": database['name']},
            },
            session=session,
        )
        if cluster_result:
            database['cluster_name'] = cluster_name
            database_result = database_collection.insert_one(database, session=session)
        else:
            return None

        return [cluster_result, database_result]

    with transaction_connection.start_session() as s:
        return s.with_transaction(callback)


@cluster_connection.handle_exceptions
def delete_database_by_name(name: str):
    cluster = collection.find_one_and_delete(filter={"name": name})
    if cluster:
        return cluster
    return None


@cluster_connection.handle_exceptions
def get_database_by_name(name: str):
    cluster = collection.find_one(filter={"name": name})
    if cluster:
        return cluster
    return None
