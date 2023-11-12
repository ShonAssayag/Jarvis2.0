import json
from pydantic import BaseModel
from src.utils.init_db_conn import jarvis_db as db, cluster_connection


collection = db.get_collection('clusters')


# class Cluster:
#     def __init__(self, name: str, version: str, architecture: str, hosts: dict, is_tls: bool, auth_mechanism: str,
#                  resources: dict, mms_project_id: str):
#         self.name = name
#         self.version = version
#         self.architecture = architecture
#         self.hosts = hosts
#         self.is_tls = is_tls
#         self.auth_mechanism = auth_mechanism
#         self.resources = resources,
#         self.mms_group_id = mms_project_id
#
#     def to_json(self):
#         cluster = {
#             "name": self.name,
#             "version": self.version,
#             "architecture": self.architecture,
#             "hosts": self.hosts,
#             "is_tls": self.is_tls,
#             "auth_mechanism": self.auth_mechanism,
#             "resources": self.resources,
#             "mms_group_id": self.mms_group_id
#         }
#         return json.dumps(cluster)

class Cluster(BaseModel):
    name: str
    version: str
    architecture: str
    hosts: dict
    is_tls: bool
    auth_mechanism: str
    resources: dict
    mms_group_id: str

    # Example of request Json
    # {
    #     "name": "shon",
    #     "version": "6.0.8-ent",
    #     "architecture": "replicaSet",
    #     "hosts": {"hosts": ["cluster0.tr5cdgj.mongodb.net:27017"]},
    #     "is_tls": false,
    #     "auth_mechanism": "SCRAM-SHA-1",
    #     "resources": {"limits": {"memory": "1Gi", "cpu": "1"}, "requests": {"memory": "1Gi", "cpu": "1"}},
    #     "mms_group_id": "1GIRK13686FKSODNF"
    # }
    def to_json(self):
        cluster = {
            "name": self.name,  # unique index
            "version": self.version,
            "architecture": self.architecture,
            "hosts": self.hosts,
            "is_tls": self.is_tls,
            "auth_mechanism": self.auth_mechanism,
            "resources": self.resources,
            "mms_group_id": self.mms_group_id
        }
        return cluster


@cluster_connection.handle_exceptions
def add_cluster(cluster: Cluster):
    collection.insert_one(cluster)


@cluster_connection.handle_exceptions
def delete_cluster_by_name(name):
    collection.delete_one({"name": name})


@cluster_connection.handle_exceptions
def get_cluster_by_name(name):
    cluster = collection.find_one({"name": name})
    print(cluster)
    return cluster

