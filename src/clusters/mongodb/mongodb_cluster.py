from src.utils.init_db_conn import jarvis_db as db, cluster_connection, get_transaction_connection

collection = db.get_collection('mongodb_clusters')


@cluster_connection.handle_exceptions
def add_cluster(cluster: dict):
    collection.insert_one(cluster)


@cluster_connection.handle_exceptions
def delete_cluster_by_name(name: str):
    transaction_connection = get_transaction_connection()

    def callback(session):
        clusters_collection = session.client.Jarvis.mongodb_clusters

        database_collection = session.client.Jarvis.mongodb_databases

        database_collection.delete_many({"cluster_name": name}, session=session)

        cluster_result = clusters_collection.find_one_and_delete({"name": name}, session=session)

        return cluster_result

    with transaction_connection.start_session() as s:
        return s.with_transaction(callback)


@cluster_connection.handle_exceptions
def get_cluster_by_name(name: str):
    cluster = collection.find_one(filter={"name": name})
    if cluster:
        return cluster
    return None
