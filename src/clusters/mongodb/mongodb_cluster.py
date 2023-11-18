from src.utils.init_db_conn import jarvis_db as db, cluster_connection

collection = db.get_collection('mongodb_clusters')


@cluster_connection.handle_exceptions
def add_cluster(cluster: dict):
    collection.insert_one(cluster)


@cluster_connection.handle_exceptions
def delete_cluster_by_name(name: str):
    cluster = collection.find_one_and_delete(filter={"name": name})
    if cluster:
        return cluster
    return None


@cluster_connection.handle_exceptions
def get_cluster_by_name(name: str):
    cluster = collection.find_one(filter={"name": name})
    if cluster:
        return cluster
    return None
